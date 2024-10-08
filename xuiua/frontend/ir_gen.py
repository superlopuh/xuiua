from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Callable, Sequence, cast
from xdsl.dialects.builtin import ArrayAttr, FunctionType, ModuleOp
from xdsl.dialects.arith import Constant
from xdsl.dialects.func import FuncOp, Return

from xdsl.builder import Builder
from xdsl.ir import Block, Region, SSAValue
from xdsl.irdl import IRDLOperation
from xdsl.parser import DenseIntOrFPElementsAttr
from xdsl.rewriter import InsertPoint, Rewriter

from xuiua.dialect import UIUA, YieldOp, utf64, t64

from xuiua.frontend.ast import (
    Array,
    BindingItem,
    Comment,
    Func,
    Item,
    Items,
    Modified,
    ModuleItem,
    Number,
    Primitive,
    PrimitiveClass,
    PrimitiveSpelling,
    ScopedModule,
    Spaces,
    Spanned,
    Word,
    WordsItem,
)

PRIMITIVE_OPS: dict[str, type[IRDLOperation]] = {
    op.name.split(".", 1)[1]: cast(type[IRDLOperation], op) for op in UIUA.operations
}


PRIMITIVE_MAP = {
    prim: PRIMITIVE_OPS[prim.name.lower()]
    for prim in PrimitiveSpelling
    if prim.name.lower() in PRIMITIVE_OPS
}


class BlockBuilder:
    builder: Builder
    block: Block
    stack: list[SSAValue]

    def __init__(self, module: ModuleOp, block: Block):
        self.module = module
        self.builder = Builder.at_end(block)
        self.block = block
        self.stack = []

    # region Word

    def build_number(self, number: Number) -> None:
        constant_op = Constant(
            DenseIntOrFPElementsAttr.from_list(t64(1), (number.float_val,))
        )
        self.builder.insert(constant_op)
        self.stack.append(constant_op.result)

    def build_array(self, array: Array) -> None:
        raise NotImplementedError

    def build_func(self, func: Func) -> None:
        for line in func.lines:
            self.build_word_line(line)

    def build_comment(self, comment: Comment) -> None:
        """
        Nothing to build for comments.
        """
        return None

    def build_spaces(self, spaces: Spaces) -> None:
        """
        Nothing to build for spaces.
        """
        return None

    def pop_args(self, num: int) -> Sequence[SSAValue]:
        """
        Pops the requested number of arguments from the stack, creating new ones if there
        are not enough values available.
        """
        popped = self.stack[-num:]
        self.stack[-num:] = []

        if len(popped) == num:
            return popped

        # Not enough values in stack, create in function

        new_vals = list(
            self.block.insert_arg(utf64, 0) for _ in range(num - len(popped))
        )
        new_vals.reverse()

        return new_vals + popped

    def build_word(self, word: Word) -> None:
        WORD_BUILDERS[type(word)](self, word)

    # endregion

    def build_word_line(self, spanned_words: tuple[Spanned[Word], ...]):
        for spanned_word in reversed(spanned_words):
            self.build_word(spanned_word.value)

    def build_dyadic_pervasive(
        self, spelling: PrimitiveSpelling, operands: Sequence[SSAValue]
    ) -> None:
        op = PRIMITIVE_MAP[spelling].build(
            operands=operands, result_types=(utf64,) * spelling.num_outputs()
        )
        self.builder.insert(op)
        self.stack.extend(op.results)

    def build_aggregating_modifier(
        self, spelling: PrimitiveSpelling, operands: Sequence[SSAValue]
    ) -> None:
        raise NotImplementedError

    def build_modified(self, modified: Modified) -> None:
        spelling = modified.modifier.spelling
        operands = self.pop_args(spelling.num_inputs())

        block = Block()
        region = Region(block)

        inner_builder = BlockBuilder(self.module, block)

        inner_builder.build_word_line(modified.operands)

        Rewriter.insert_op(
            YieldOp(*inner_builder.stack),
            InsertPoint.at_end(block),
        )

        op = PRIMITIVE_MAP[spelling].build(
            operands=operands,
            result_types=(utf64,) * spelling.num_outputs(),
            regions=(region,),
        )
        self.builder.insert(op)
        self.stack.extend(op.results)

    def build_primitive(self, primitive: Primitive) -> None:
        spelling = primitive.spelling
        operands = self.pop_args(spelling.num_inputs())

        if spelling is PrimitiveSpelling.IDENTITY:
            self.stack.extend(operands)
            return

        if spelling is PrimitiveSpelling.DUPLICATE:
            self.stack.extend(operands)
            self.stack.extend(operands)
            return

        match primitive.spelling.primitive_class():
            case PrimitiveClass.DYADIC_PERVASIVE:
                self.build_dyadic_pervasive(primitive.spelling, operands)
            case PrimitiveClass.AGGREGATING_MODIFIER:
                self.build_aggregating_modifier(primitive.spelling, operands)
            case not_implemented_class:
                raise NotImplementedError(f"{not_implemented_class}")


WORD_BUILDERS: dict[type[Word], Callable[[BlockBuilder, Any], None]] = {
    Number: BlockBuilder.build_number,
    Array: BlockBuilder.build_array,
    Func: BlockBuilder.build_func,
    Comment: BlockBuilder.build_comment,
    Spaces: BlockBuilder.build_spaces,
    Primitive: BlockBuilder.build_primitive,
    Modified: BlockBuilder.build_modified,
}


class FunctionBuilder(BlockBuilder):
    module: ModuleOp
    func_op: FuncOp

    def __init__(self, module: ModuleOp, func_op: FuncOp):
        block = func_op.body.block
        super().__init__(module, block)
        self.func_op = func_op

    def finalize(self):
        Rewriter.insert_op(
            Return(*self.stack),
            InsertPoint.at_end(self.block),
        )

        # Update the function type
        self.func_op.function_type = FunctionType.from_attrs(
            ArrayAttr(arg.type for arg in self.block.args),
            ArrayAttr(res.type for res in self.stack),
        )

    @contextmanager
    @staticmethod
    def build_func_op(module: ModuleOp, name: str) -> Iterator["FunctionBuilder"]:
        func_op = FuncOp(name, ((), ()))
        function_builder = FunctionBuilder(module, func_op)
        yield function_builder
        function_builder.finalize()


class ModuleBuilder:
    module: ModuleOp
    main_builder: FunctionBuilder | None

    def __init__(self):
        self.module = ModuleOp([])
        self.main_builder = None

    # region Item

    def build_scoped_module(self, scoped_module: ScopedModule) -> None:
        raise NotImplementedError

    def build_words_item(self, words_item: WordsItem) -> None:
        if self.main_builder is None:
            func_op = FuncOp("uiua_main", ((), ()))
            self.main_builder = FunctionBuilder(self.module, func_op)

        for line in words_item.lines:
            self.main_builder.build_word_line(line)

    def build_binding_item(self, binding_item: BindingItem) -> None:
        with FunctionBuilder.build_func_op(self.module, binding_item.name) as fb:
            fb.build_word_line(binding_item.words)
            Rewriter.insert_op(
                fb.func_op,
                InsertPoint.at_end(self.module.body.block),
            )

    def build_module_item(self, module_item: ModuleItem) -> None:
        raise NotImplementedError

    def build_item(self, item: Item):
        ITEM_BUILDERS[type(item)](self, item)

    # endregion

    def build_items(self, items: tuple[Item, ...]):
        for item in items:
            self.build_item(item)

    def build_module(self, items: Items):
        for item_tuple in items:
            self.build_items(item_tuple)

        if self.main_builder is not None:
            self.main_builder.finalize()
            Rewriter.insert_op(
                self.main_builder.func_op, InsertPoint.at_end(self.module.body.block)
            )


ITEM_BUILDERS: dict[type[Item], Callable[[ModuleBuilder, Any], None]] = {
    ScopedModule: ModuleBuilder.build_scoped_module,
    WordsItem: ModuleBuilder.build_words_item,
    BindingItem: ModuleBuilder.build_binding_item,
    ModuleItem: ModuleBuilder.build_module_item,
}


def build_module(items: Items) -> ModuleOp:
    b = ModuleBuilder()
    b.build_module(items)
    return b.module

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Callable
from xdsl.dialects.builtin import ArrayAttr, FunctionType, ModuleOp, f64
from xdsl.dialects.arith import Constant
from xdsl.dialects.func import FuncOp, Return

from xdsl.builder import Builder
from xdsl.ir import Block, SSAValue
from xdsl.parser import FloatAttr
from xdsl.rewriter import InsertPoint, Rewriter

from xuiua.dialect import utf64

from xuiua.ast import (
    Array,
    BindingItem,
    Comment,
    Item,
    Items,
    ModuleItem,
    Number,
    Primitive,
    ScopedModule,
    Spaces,
    Spanned,
    Word,
    WordsItem,
)


class FunctionBuilder:
    module: ModuleOp
    func_op: FuncOp
    builder: Builder
    block: Block
    stack: list[SSAValue]

    def __init__(self, module: ModuleOp, func_op: FuncOp):
        block = func_op.body.block
        self.module = module
        self.func_op = func_op
        self.builder = Builder.at_end(block)
        self.block = block
        self.stack = []

    # region Word

    def build_number(self, number: Number) -> None:
        constant_op = Constant(FloatAttr(number.float_val, f64))
        self.builder.insert(constant_op)
        self.stack.append(constant_op.result)

    def build_array(self, array: Array) -> None:
        raise NotImplementedError

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

    def build_primitive(self, primitive: Primitive) -> None:
        raise NotImplementedError

    def build_word(self, word: Word) -> None:
        WORD_BUILDERS[type(word)](self, word)

    # endregion

    def build_word_line(self, spanned_words: tuple[Spanned[Word], ...]):
        for spanned_word in reversed(spanned_words):
            self.build_word(spanned_word.value)

    def finalize(self):
        Rewriter.insert_op(
            Return(*self.stack),
            InsertPoint.at_end(self.block),
        )

        # Update the function type
        num_args = len(self.block.args)
        num_returns = len(self.stack)

        self.func_op.function_type = FunctionType.from_attrs(
            ArrayAttr((utf64,) * num_args),
            ArrayAttr((utf64,) * num_returns),
        )

    @contextmanager
    @staticmethod
    def build_func(module: ModuleOp, name: str) -> Iterator["FunctionBuilder"]:
        func_op = FuncOp(name, ((), ()))
        function_builder = FunctionBuilder(module, func_op)
        yield function_builder
        function_builder.finalize()


WORD_BUILDERS: dict[type[Word], Callable[[FunctionBuilder, Any], None]] = {
    Number: FunctionBuilder.build_number,
    Array: FunctionBuilder.build_array,
    Comment: FunctionBuilder.build_comment,
    Spaces: FunctionBuilder.build_spaces,
    Primitive: FunctionBuilder.build_primitive,
}


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
        with FunctionBuilder.build_func(self.module, binding_item.name) as fb:
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

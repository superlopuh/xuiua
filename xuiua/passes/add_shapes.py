from collections.abc import Sequence
from dataclasses import dataclass, field
from xdsl.dialects.builtin import FunctionType, ArrayAttr, ModuleOp
from xdsl.dialects.func import FuncOp, Return
from xdsl.rewriter import InsertPoint, Rewriter
from xuiua.dialect import CastOp, t64
from xdsl.passes import ModulePass
from xdsl.context import MLContext
from xdsl.traits import SymbolTable


def add_shapes(func_op: FuncOp, shapes: Sequence[Sequence[int]]):
    ftype = func_op.function_type
    existing_inputs = ftype.inputs.data
    assert len(existing_inputs) == len(shapes)
    new_inputs = tuple(t64(*shape) for shape in shapes)
    func_op.function_type = FunctionType.from_attrs(
        ArrayAttr(new_inputs), ftype.outputs
    )
    body = func_op.body.block
    for arg, new_type in zip(body.args, new_inputs, strict=True):
        arg.type = new_type

    return_op = body.last_op
    if return_op is None:
        return
    assert isinstance(return_op, Return), f"{return_op}"

    cast_ops = tuple(CastOp(operand) for operand in return_op.operands)

    Rewriter.insert_op(cast_ops, InsertPoint.before(return_op))

    return_op.operands = tuple(op.res for op in cast_ops)


def parse_shapes_encoding(encoding: str) -> dict[str, tuple[tuple[int, ...], ...]]:
    return {
        (components := func.split("="))[0]: tuple(
            tuple(int(dim) for dim in shape.split("x")) if shape else ()
            for shape in components[1].split("_")
        )
        if components[1]
        else ()
        for func in encoding.split(";")
    }


@dataclass(frozen=True)
class AddShapesPass(ModulePass):
    """
    Assigns the shapes to specified functions.

    Example shapes format: `"Add=2x3_2x3;Id=4x5"`
    """

    name = "add-shapes"

    shapes: str = field()

    def apply(self, ctx: MLContext, op: ModuleOp) -> None:
        shapes_dict = parse_shapes_encoding(self.shapes)
        for name, shapes in shapes_dict.items():
            func_op = SymbolTable.lookup_symbol(op, name)
            assert isinstance(func_op, FuncOp)
            add_shapes(func_op, shapes)

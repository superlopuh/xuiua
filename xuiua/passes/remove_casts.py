from dataclasses import dataclass
from typing import cast
from xdsl.dialects.builtin import FunctionType, ArrayAttr, ModuleOp
from xdsl.dialects.func import FuncOp, Return
from xdsl.rewriter import Rewriter
from xuiua.dialect import CastOp
from xdsl.passes import ModulePass
from xdsl.context import MLContext


def remove_casts(func_op: FuncOp):
    ftype = func_op.function_type

    body = func_op.body.block

    return_op = body.last_op
    if return_op is None:
        return
    assert isinstance(return_op, Return), f"{return_op}"

    cast_ops = tuple(operand.owner for operand in return_op.operands)
    for op in cast_ops:
        assert isinstance(op, CastOp), f"{op}"

    cast_ops = cast(tuple[CastOp, ...], cast_ops)

    return_op.operands = tuple(op.arg for op in cast_ops)

    for op in cast_ops:
        Rewriter.erase_op(op)

    func_op.function_type = FunctionType.from_attrs(
        ftype.inputs, ArrayAttr(arg.type for arg in return_op.operands)
    )


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
class RemoveCastsPass(ModulePass):
    """
    Remove casts.
    """

    name = "remove-casts"

    def apply(self, ctx: MLContext, op: ModuleOp) -> None:
        for func_op in op.body.ops:
            if isinstance(func_op, FuncOp):
                remove_casts(func_op)

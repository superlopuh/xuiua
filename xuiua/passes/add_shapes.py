from collections.abc import Sequence
from xdsl.dialects.builtin import FunctionType, ArrayAttr
from xdsl.dialects.func import FuncOp
from xuiua.dialect import t64


def add_shapes(func_op: FuncOp, shapes: Sequence[Sequence[int]]):
    ftype = func_op.function_type
    existing_inputs = ftype.inputs.data
    assert len(existing_inputs) == len(shapes)
    new_inputs = tuple(t64(*shape) for shape in shapes)
    func_op.function_type = FunctionType.from_attrs(
        ArrayAttr(new_inputs), ftype.outputs
    )

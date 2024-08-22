from xdsl.dialects.builtin import (
    I32,
    Float32Type,
    Float64Type,
    TensorType,
    UnrankedTensorType,
    f64,
)
from xdsl.ir import Attribute, Dialect, SSAValue
from xdsl.irdl import (
    base,
    irdl_op_definition,
    IRDLOperation,
    operand_def,
    result_def,
)
from xdsl.traits import Pure

TI32 = TensorType[I32]
UTI32 = UnrankedTensorType[I32]
TF32 = TensorType[Float32Type]
UTF32 = UnrankedTensorType[Float32Type]
TF64 = TensorType[Float64Type]
UTF64 = UnrankedTensorType[Float64Type]
utf64 = UTF64(f64)

TT = TI32 | TF32
TTConstr = base(TI32) | base(TF32)
UTT = UTI32 | UTF32 | UTF64
UTTConstr = base(UTI32) | base(UTF32) | base(UTF64)
UIUATensorType = TT | UTT
UIUATensorConstr = TTConstr | UTTConstr


def t64(*shape: int) -> TF64:
    """
    Returns a shaped tensor type of f64 values.
    """
    return TensorType(f64, shape)


@irdl_op_definition
class AddOp(IRDLOperation):
    """
    Add values.

    https://www.uiua.org/docs/add
    """

    name = "uiua.add"

    lhs = operand_def(UIUATensorConstr)
    rhs = operand_def(UIUATensorConstr)
    res = result_def(UIUATensorConstr)

    def __init__(
        self, lhs: SSAValue, rhs: SSAValue, result_type: Attribute | None = None
    ):
        if result_type is None:
            result_type = lhs.type

        super().__init__(operands=(lhs, rhs), result_types=(result_type,))


@irdl_op_definition
class CastOp(IRDLOperation):
    name = "uiua.cast"
    arg = operand_def(UIUATensorConstr)
    res = result_def(UIUATensorConstr)

    traits = frozenset((Pure(),))

    def __init__(self, arg: SSAValue, res: UIUATensorType | None = None):
        if res is None:
            res = utf64

        return super().__init__(
            operands=[arg],
            result_types=[res],
        )


UIUA = Dialect(
    "uiua",
    [
        AddOp,
        CastOp,
    ],
)

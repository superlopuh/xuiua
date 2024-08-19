from xdsl.dialects.builtin import I32, Float32Type, TensorType, UnrankedTensorType
from xdsl.ir import Attribute, Dialect, SSAValue
from xdsl.irdl import (
    base,
    irdl_op_definition,
    IRDLOperation,
    operand_def,
    result_def,
)

TI32 = TensorType[I32]
UTI32 = UnrankedTensorType[I32]
TF32 = TensorType[Float32Type]
UTF32 = UnrankedTensorType[Float32Type]

TT = TI32 | TF32
TTConstr = base(TI32) | base(TF32)
UTT = UTI32 | UTF32
UTTConstr = base(UTI32) | base(UTF32)
UIUATensorType = TT | UTT
UIUATensorConstr = TTConstr | UTTConstr


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


UIUA = Dialect(
    "uiua",
    [
        AddOp,
    ],
)

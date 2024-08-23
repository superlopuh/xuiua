from xdsl.dialects.builtin import (
    I32,
    Float32Type,
    Float64Type,
    TensorType,
    UnrankedTensorType,
    f64,
)
from xdsl.ir import Attribute, Dialect, Region, SSAValue, VerifyException
from xdsl.irdl import (
    base,
    irdl_op_definition,
    IRDLOperation,
    operand_def,
    region_def,
    result_def,
    var_operand_def,
)
from xdsl.traits import HasParent, HasShapeInferencePatternsTrait, Pure
from xdsl.utils.isattr import isattr

TI32 = TensorType[I32]
UTI32 = UnrankedTensorType[I32]
TF32 = TensorType[Float32Type]
UTF32 = UnrankedTensorType[Float32Type]
TF64 = TensorType[Float64Type]
UTF64 = UnrankedTensorType[Float64Type]
utf64 = UTF64(f64)

TT = TI32 | TF32 | TF64
TTConstr = base(TI32) | base(TF32) | base(TF64)
UTT = UTI32 | UTF32 | UTF64
UTTConstr = base(UTI32) | base(UTF32) | base(UTF64)
UIUATensorType = TT | UTT
UIUATensorConstr = TTConstr | UTTConstr


def t64(*shape: int) -> TF64:
    """
    Returns a shaped tensor type of f64 values.
    """
    return TensorType(f64, shape)


class AddOpHasShapeInferencePatternsTrait(HasShapeInferencePatternsTrait):
    @classmethod
    def get_shape_inference_patterns(cls):
        from xuiua.shape_inference_patterns import (
            AddOpShapeInferencePattern,
        )

        return (AddOpShapeInferencePattern(),)


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

    traits = frozenset(
        (
            Pure(),
            AddOpHasShapeInferencePatternsTrait(),
        )
    )

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


class MultiplyOpHasShapeInferencePatternsTrait(HasShapeInferencePatternsTrait):
    @classmethod
    def get_shape_inference_patterns(cls):
        from xuiua.shape_inference_patterns import (
            MultiplyOpShapeInferencePattern,
        )

        return (MultiplyOpShapeInferencePattern(),)


@irdl_op_definition
class MultiplyOp(IRDLOperation):
    """
    Multiply values.

    https://www.uiua.org/docs/multiply
    """

    name = "uiua.multiply"

    lhs = operand_def(UIUATensorConstr)
    rhs = operand_def(UIUATensorConstr)
    res = result_def(UIUATensorConstr)

    traits = frozenset(
        (
            Pure(),
            MultiplyOpHasShapeInferencePatternsTrait(),
        )
    )

    def __init__(
        self, lhs: SSAValue, rhs: SSAValue, result_type: Attribute | None = None
    ):
        if result_type is None:
            result_type = lhs.type

        super().__init__(operands=(lhs, rhs), result_types=(result_type,))


class ReduceOpHasShapeInferencePatternsTrait(HasShapeInferencePatternsTrait):
    @classmethod
    def get_shape_inference_patterns(cls):
        from xuiua.shape_inference_patterns import (
            ReduceOpShapeInferencePattern,
        )

        return (ReduceOpShapeInferencePattern(),)


@irdl_op_definition
class ReduceOp(IRDLOperation):
    """
    Reduces a value left to right pairwise with a specified transform.

    https://www.uiua.org/docs/reduce
    """

    name = "uiua.reduce"

    arg = operand_def(UIUATensorConstr)
    res = result_def(UIUATensorConstr)
    body = region_def("single_block")

    traits = frozenset((Pure(), ReduceOpHasShapeInferencePatternsTrait()))

    def __init__(self, arg: SSAValue, result_type: Attribute, body: Region):
        super().__init__(operands=(arg,), result_types=(result_type,), regions=(body,))

    def verify_(self) -> None:
        args = self.body.block.args
        if len(args) != 2:
            raise VerifyException(
                f"Invalid number of operands in reduce region: {len(args)}"
            )

        acc, val = args

        # The first arg of the region is the accumulator
        # It should have the same type as the result
        if acc.type != self.res.type:
            raise VerifyException(
                f"Mismatching types for reduction accumulator: {acc.type} != {self.res.type}"
            )

        # The second arg of the region is the iteration element
        # It should have one fewer dimension than the arg
        if isattr(self.arg.type, TTConstr) and isattr(val.type, TTConstr):
            arg_shape = self.arg.type.get_shape()
            val_shape = val.type.get_shape()

            if len(arg_shape) != (len(val_shape) + 1) or arg_shape[1:] != val_shape:
                raise VerifyException(
                    f"Mismatching shapes for reduction value and operand: {arg_shape} != {val_shape}"
                )


@irdl_op_definition
class YieldOp(IRDLOperation):
    """
    Yields a reduction value.
    """

    name = "uiua.yield"

    arg = var_operand_def(UIUATensorConstr)

    traits = frozenset((lambda: HasParent(ReduceOp),))

    def __init__(self, *args: SSAValue):
        super().__init__(operands=(args))


UIUA = Dialect(
    "uiua",
    [
        AddOp,
        CastOp,
        MultiplyOp,
        ReduceOp,
        YieldOp,
    ],
)

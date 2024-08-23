from xdsl.pattern_rewriter import (
    PatternRewriter,
    RewritePattern,
    op_type_rewrite_pattern,
)
from xdsl.utils.hints import isa

from xuiua.dialect import TF64, AddOp, MultiplyOp, ReduceOp, t64


def rewrite_diadic_same_shapes(op: AddOp | MultiplyOp, rewriter: PatternRewriter):
    assert isa((lhs_type := op.lhs.type), TF64)
    assert isa((rhs_type := op.rhs.type), TF64)

    assert lhs_type.get_shape() == rhs_type.get_shape()

    if lhs_type != op.res.type:
        rewriter.modify_value_type(op.res, lhs_type)


class AddOpShapeInferencePattern(RewritePattern):
    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: AddOp, rewriter: PatternRewriter, /):
        rewrite_diadic_same_shapes(op, rewriter)


class MultiplyOpShapeInferencePattern(RewritePattern):
    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: MultiplyOp, rewriter: PatternRewriter, /):
        rewrite_diadic_same_shapes(op, rewriter)


class ReduceOpShapeInferencePattern(RewritePattern):
    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: ReduceOp, rewriter: PatternRewriter, /):
        if isa(op.res.type, TF64):
            return

        assert isa((arg_type := op.arg.type), TF64)
        arg_shape = arg_type.get_shape()

        assert len(arg_shape)

        block_args = op.body.block.args
        assert len(block_args) == 2

        inner_shape = arg_shape[1:]
        inner_type = t64(*inner_shape)

        acc_arg, val_arg = block_args

        rewriter.modify_value_type(acc_arg, inner_type)
        rewriter.modify_value_type(val_arg, inner_type)
        rewriter.modify_value_type(op.res, inner_type)

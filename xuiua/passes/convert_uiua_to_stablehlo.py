from dataclasses import dataclass
from numpy import prod
from xdsl.dialects.builtin import ModuleOp
from xdsl.parser import DenseIntOrFPElementsAttr, TensorType
from xdsl.rewriter import Rewriter
from xuiua.dialect import AddOp, TF64, ReduceOp, YieldOp
from xdsl.passes import ModulePass
from xdsl.context import MLContext
from xdsl.pattern_rewriter import (
    PatternRewriteWalker,
    RewritePattern,
    op_type_rewrite_pattern,
    PatternRewriter,
    GreedyRewritePatternApplier,
)
from xdsl.utils.hints import isa
from xdsl.dialects import arith, stablehlo


class LowerAddPattern(RewritePattern):
    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: AddOp, rewriter: PatternRewriter):
        assert isa(op.lhs.type, TF64)
        assert isa(op.rhs.type, TF64)
        assert op.lhs.type == op.rhs.type
        rewriter.replace_matched_op(stablehlo.AddOp(op.lhs, op.rhs))


class LowerReducePattern(RewritePattern):
    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: ReduceOp, rewriter: PatternRewriter):
        assert isa(op.arg.type, TF64)
        body = op.body
        block = body.block
        args = block.args
        assert isa(args[0].type, TF64)
        assert isa(args[1].type, TF64)
        assert isa(op.res.type, TF64)

        new_type = TensorType(op.res.type.element_type, ())

        constant_op = arith.Constant(
            DenseIntOrFPElementsAttr.create_dense_float(new_type, (0.0,))
        )
        reduce_op = stablehlo.ReduceOp(
            (op.arg,),
            (constant_op.result,),
            (0,),
            Rewriter.move_region_contents_to_new_regions(body),
            op.result_types,
        )

        rewriter.replace_matched_op((constant_op, reduce_op))
        rewriter.modify_value_type(args[0], new_type)
        rewriter.modify_value_type(args[1], new_type)


class LowerYieldPattern(RewritePattern):
    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: YieldOp, rewriter: PatternRewriter):
        rewriter.replace_matched_op(stablehlo.ReturnOp(list(op.operands)))


@dataclass(frozen=True)
class ConvertUiuaToStableHLOPass(ModulePass):
    """ """

    name = "convert-uiua-to-stablehlo"

    def apply(self, ctx: MLContext, op: ModuleOp) -> None:
        PatternRewriteWalker(
            GreedyRewritePatternApplier(
                [
                    LowerAddPattern(),
                    LowerReducePattern(),
                    LowerYieldPattern(),
                ]
            )
        ).rewrite_module(op)

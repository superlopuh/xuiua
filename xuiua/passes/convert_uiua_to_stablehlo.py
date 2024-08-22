from dataclasses import dataclass
from xdsl.dialects.builtin import ModuleOp
from xuiua.dialect import AddOp, TF64
from xdsl.passes import ModulePass
from xdsl.context import MLContext
from xdsl.pattern_rewriter import (
    PatternRewriteWalker,
    RewritePattern,
    op_type_rewrite_pattern,
    PatternRewriter,
    GreedyRewritePatternApplier,
)
from xdsl.utils.isa import isa
from xdsl.dialects import stablehlo


class LowerAddPattern(RewritePattern):
    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: AddOp, rewriter: PatternRewriter):
        assert isa(op.lhs.type, TF64)
        assert isa(op.rhs.type, TF64)
        assert op.lhs.type == op.rhs.type
        rewriter.replace_matched_op(stablehlo.AddOp(op.lhs, op.rhs))


@dataclass(frozen=True)
class ConvertUiuaToStableHLOPass(ModulePass):
    """ """

    name = "convert-uiua-to-stablehlo"

    def apply(self, ctx: MLContext, op: ModuleOp) -> None:
        PatternRewriteWalker(
            GreedyRewritePatternApplier(
                [
                    LowerAddPattern(),
                ]
            )
        ).rewrite_module(op)

from xdsl.context import MLContext

from xdsl.dialects.builtin import Builtin
from xdsl.dialects.func import Func
from xdsl.dialects import test

from xuiua.dialect import UIUA

import jax
import jax.numpy as jnp
from jax import config


from xdsl.backend.jax_executable import JaxExecutable
from xdsl.dialects.builtin import ModuleOp
from xdsl.dialects.func import FuncOp
from xdsl.traits import SymbolTable
from xdsl.transforms import shape_inference

from xuiua.frontend.ir_gen import build_module
from xuiua.frontend.parser import Parser
from xuiua.passes import remove_casts, convert_uiua_to_stablehlo
from xuiua.passes.add_shapes import add_shapes
import numpy as np


def get_ctx() -> MLContext:
    ctx = MLContext()
    ctx.register_dialect("builtin", lambda: Builtin)
    ctx.register_dialect("func", lambda: Func)
    ctx.register_dialect("uiua", lambda: UIUA)
    ctx.register_dialect("test", lambda: test.Test)
    return ctx


config.update("jax_enable_x64", True)


def a(els: tuple[float, ...]) -> jax.Array:
    floats = tuple(float(el) for el in els)
    return jnp.array(np.array(floats))


def build_expr_module(expr: str) -> ModuleOp:
    parser = Parser("main ← " + expr)
    items = parser.parse_items()
    module = build_module(items)
    return module


# shape-inference,remove-casts,convert-uiua-to-stablehlo
SHAPED_PIPELINE = [
    shape_inference.ShapeInferencePass(),
    remove_casts.RemoveCastsPass(),
    convert_uiua_to_stablehlo.ConvertUiuaToStableHLOPass(),
]


def run(expr: str, inputs: tuple[jax.Array, ...]) -> tuple[jax.Array, ...]:
    module = build_expr_module(expr)
    shapes = tuple(i.shape for i in inputs)
    main_op = SymbolTable.lookup_symbol(module, "main")
    assert isinstance(main_op, FuncOp)
    add_shapes(main_op, shapes)
    ctx = get_ctx()
    for p in SHAPED_PIPELINE:
        p.apply(ctx, module)

    jax_executable = JaxExecutable.compile(module)

    result = jax_executable.execute(inputs)

    return tuple(result)

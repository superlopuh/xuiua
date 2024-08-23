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
from xuiua.compile import get_ctx
import numpy as np

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


def test_compile_add():
    A = a((2, 3, 4.5))
    B = a((4, 5, 6.0))
    C = a((6, 8, 10.5))
    assert (A + B == C).all()

    (res,) = run("+", (A, B))

    assert (res == C).all()


def test_dtype():
    my_np_array = np.array((1.0,), dtype=np.float64)
    assert my_np_array.dtype == np.float64
    my_jax_array = jnp.array(my_np_array)

    assert my_jax_array.dtype == np.float64


def test_compile_add():
    A = a((2, 3, 4, 4.5, 5.5, 6.5)).reshape((2, 3))
    B = a((6.5, 8.5, 10.5))
    res0 = A.sum(axis=0)

    assert (res0 == B).all()

    (res,) = run("/+", (A,))

    assert (res == B).all()

from collections.abc import Callable

import jax
from xdsl.context import MLContext

from xdsl.dialects.builtin import Builtin
from xdsl.dialects.func import Func
from xdsl.dialects import test

from xuiua.dialect import UIUA


def get_ctx() -> MLContext:
    ctx = MLContext()
    ctx.register_dialect("builtin", lambda: Builtin)
    ctx.register_dialect("func", lambda: Func)
    ctx.register_dialect("uiua", lambda: UIUA)
    ctx.register_dialect("test", lambda: test.Test)
    return ctx

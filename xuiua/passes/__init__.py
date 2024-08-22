from collections.abc import Callable
from .add_shapes import AddShapesPass
from xdsl.passes import ModulePass

AVAILABLE_PASSES: dict[str, Callable[[], type[ModulePass]]] = {
    AddShapesPass.name: lambda: AddShapesPass,
}

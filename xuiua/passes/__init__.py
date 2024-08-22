from collections.abc import Callable
from .add_shapes import AddShapesPass
from .remove_casts import RemoveCastsPass
from xdsl.passes import ModulePass
from xdsl.transforms.shape_inference import ShapeInferencePass


AVAILABLE_PASSES: dict[str, Callable[[], type[ModulePass]]] = {
    AddShapesPass.name: lambda: AddShapesPass,
    RemoveCastsPass.name: lambda: RemoveCastsPass,
    ShapeInferencePass.name: lambda: ShapeInferencePass,
}

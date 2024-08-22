from xdsl.dialects.builtin import ArrayAttr, FunctionType, TensorType, f64
from xdsl.dialects.func import FuncOp
from xuiua.passes.add_shapes import add_shapes


def test_add_shapes():
    func_op = FuncOp("hello", ((TensorType(f64, ()),) * 3, ()))
    shapes = ((), (1, 2), (3,))
    add_shapes(func_op, shapes)

    input_types = tuple(TensorType(f64, shape) for shape in shapes)

    assert func_op.function_type == FunctionType.from_lists(input_types, ())

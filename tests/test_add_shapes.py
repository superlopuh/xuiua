from xdsl.dialects.builtin import FunctionType, TensorType, f64
from xdsl.dialects.func import FuncOp
from xuiua.passes.add_shapes import add_shapes, parse_shapes_encoding


def test_add_shapes():
    func_op = FuncOp("hello", ((TensorType(f64, ()),) * 3, ()))
    shapes = ((), (1, 2), (3,))
    add_shapes(func_op, shapes)

    input_types = tuple(TensorType(f64, shape) for shape in shapes)

    assert func_op.function_type == FunctionType.from_lists(input_types, ())
    assert tuple(func_op.body.block.arg_types) == input_types


def test_shapes_encoding():
    assert parse_shapes_encoding("Add=1x2_3_;bla=;blo=1") == {
        "Add": ((1, 2), (3,), ()),
        "bla": (),
        "blo": ((1,),),
    }

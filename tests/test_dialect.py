from xdsl.dialects.builtin import i32, UnrankedTensorType

from xuiua.dialect import AddOp
from xdsl.utils.test_value import TestSSAValue


def test_init():
    UTT = UnrankedTensorType(i32)
    lhs = TestSSAValue(UTT)
    rhs = TestSSAValue(UTT)
    add = AddOp(lhs, rhs)
    add.verify()
    assert add.res.type is UTT

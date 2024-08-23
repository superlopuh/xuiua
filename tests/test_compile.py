import jax.numpy as jnp


from xuiua.compile import a, run
import numpy as np


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


def test_compile_sum():
    A = a((2, 3, 4, 4.5, 5.5, 6.5)).reshape((2, 3))
    B = a((6.5, 8.5, 10.5))
    res0 = A.sum(axis=0)

    assert (res0 == B).all()

    (res,) = run("/+", (A,))

    assert (res == B).all()

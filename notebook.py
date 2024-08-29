import marimo

__generated_with = "0.8.2"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __():
    from xuiua.compile import run, a
    return a, run


@app.cell
def __():
    import jax
    import jax.numpy as jnp

    # Set a key for reproducibility
    key = jax.random.PRNGKey(0)

    # Calculate how many float64 numbers we need for 1MB
    # 1MB = 1,048,576 bytes
    # Each float64 is 8 bytes
    num_floats = 100000000

    # Generate the random data
    random_data = jax.random.uniform(key, shape=(num_floats,), dtype=jnp.float64)
    return jax, jnp, key, num_floats, random_data


@app.cell
def __(random_data):
    random_data
    return


@app.cell
def __():
    import time
    return time,


@app.cell
def __(random_data, run, time):
    start_time = time.time()
    res = run("/+", (random_data,))
    end_time = time.time()

    execution_time = end_time - start_time
    execution_time
    return end_time, execution_time, res, start_time


@app.cell
def __(res):
    res
    return


if __name__ == "__main__":
    app.run()

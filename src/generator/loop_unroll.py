import operations


def loop_unroll(loop: operations.ForLoop) -> operations.Split:
    split = operations.Split()

    # TODO split the loop operation based on its parameters
    split.ops = [loop]

    return split

import operations


def find_inner_loop(start: operations.Operation) -> [operations.ForLoop, operations.Operation]:
    """Search a chain of Operations for the innermost loop in a chain of for loops.
    This is the starting point of a "unroll" optimization.

    @:param start The stating point of the chain. The next child must be a ForLoop
    """

    if start.nextOperation is None:
        raise AssertionError("next operation is not defined")
    elif not isinstance(start, operations.ForLoop):
        raise TypeError("next operation is not a ForLoop")

    last_for = start
    cur_op = start
    while True:
        next_op = cur_op.nextOperation
        if next_op is None:
            return last_for, cur_op  # If the next operation is not defined, last ForLoop is the innermost For loop
        elif isinstance(next_op, operations.ForLoop):
            last_for = next_op  # If the next operation is a ForLoop, then remember it

        cur_op = next_op  # Reiterate for the next operation in the chain


def loop_unroll(loop: operations.ForLoop) -> operations.Split:
    """Perform the loop unrolling optimization: split a chain of ForLoops's bodies into a parallel version"""
    split = operations.Split()

    # TODO split the loop operation based on its parameters
    split.ops = [loop]

    return split

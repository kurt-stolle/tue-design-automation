from copy import deepcopy

import operations


def optim_loop_unroll(impl: operations.ForLoop) -> operations.Operation:
    """Perform the loop unrolling optimization: split a chain of ForLoops's bodies into a parallel version

    :param impl The implementation chain on which to perform the optimization
    :returns An optimized implementation"""

    # Create a copy of impl
    impl = deepcopy(impl)

    # Walk the implementation searching for a ForLoop with an assignment or split body
    target = impl
    while True:
        if target.next_operation is None:
            raise EOFError("reached the end of the implementation chain before an unroll target could be found")
        elif isinstance(target, operations.ForLoop) and (
                isinstance(target.next_operation, operations.Assign)
                or isinstance(target.next_operation, operations.Split)):
            break  # break once we find a ForLoop which has an assigning statement or split as next operation

        target = target.next_operation  # move one operation further in the chain

    # Unroll the loop, putting the body of the loop in parallel
    split = operations.Split()
    for i in range(target.start.value, target.end.value):
        split.ops.append(target.next_operation)  # Todo set the instance variables

    # Replace the target with the new split
    target.prev_operation.then(split)

    # Return the new implementation
    return impl

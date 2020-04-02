from __future__ import annotations  # The operation class's annotations reference itself


def tabs(n: int):
    """returns n amount of 'tabs' (two spaces) for readability of the output"""
    t = ""
    for i in range(n):
        t += "  "

    return t


class Operation(object):
    """An operation, e.g. "For", "Assign" and "Multiply". This essentially creates a way of "functionally
    programming" the for-loop of the CNN, making optimization easier"""

    next_operation: Operation = None  # the next operation in the chain
    prev_operation: Operation = None  # the previous operation in the chain

    exec_time = 0

    def print_pseudo(self, **kwargs) -> str:
        raise ValueError("cannot execute print_pseudo on the Operation class: a child class must define this method")

    def print_verilog(selfs, **kwargs) -> str:
        raise ValueError("cannot execute print_verilog on the Operation class: a child class must define this method")

    def cum_exec_time(self) -> float:
        """quantify the cumulative performance of this operation and it's next operations, allowing for optimization.

        :returns memory used, execution time"""

        return self.exec_time + (self.next_operation.cum_exec_time() if self.next_operation is not None else 0)

    def then(self, next_operation: Operation) -> Operation:
        """set the next operation to be performed after this operation is done"""

        # Double link
        self.next_operation = next_operation
        next_operation.prev_operation = self

        return self



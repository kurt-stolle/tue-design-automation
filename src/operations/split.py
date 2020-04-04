from typing import List
from operations import Operation, tabs
from operations.variable import *


class Split(Operation):
    """The split operation parallelize a number of operations, the execution time is the time of the longest path"""

    ops: [Operation] = []

    def __init__(self, *args):
        self.ops = list(args)

    @property
    def exec_time(self) -> int:
        t = 0
        for op in self.ops:
            t = max(t, op.cum_exec_time())

        return int(t)

    @property
    def next_operation(self):
        return None

    # implements Operation.count - takes the cumulative
    def count(self, fn) -> int:
        c = 0
        for op in self.ops:
            c += op.count(fn)

        return c

    # implements Operation.sub
    def sub(self, *args):
        for op in self.ops:
            op.sub(*args)

    # implements Operation.vars
    def vars(self) -> List[Variable]:

        # Fixme here we assume that all branches in a split contain exactly the same variables
        return self.ops[0].vars()

    def print_pseudo(self, indent=0) -> str:
        res = []
        for i, op in enumerate(self.ops):
            res.append(op.print_pseudo(indent=indent + 1))

        return "\n".join(res)

    def then(self, next_operation: Operation) -> Operation:
        raise NameError("attempted to chain a single event after a split")  # a split cannot have a next operation
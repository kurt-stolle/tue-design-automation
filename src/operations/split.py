import math

from operations import Operation, tabs


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

    def print(self, indent=0) -> str:
        res = []
        for i, op in enumerate(self.ops):
            res.append(op.print(indent=indent + 1))

        return "{0}__split__{{\n{1}\n{0}}}".format(tabs(indent), ",\n".join(res))

    def then(self, next_operation: Operation) -> Operation:
        raise NameError("attempted to chain a single event after a split")  # a split cannot have a next operation

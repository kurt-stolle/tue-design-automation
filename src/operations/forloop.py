from abc import ABC

from operations.operation import Operation, tabs


class ForLoop(Operation, ABC):
    """A "For" Operation, assumes we only do int-based numerical for loops, e.g. from i=0 to i >= 10"""

    def __init__(self, start: int, end: int, increment: int, iterator_name: str = "i"):
        self.iterator_name = iterator_name
        self.start = start
        self.end = end
        self.increment = increment

    def print(self, indent=0) -> str:
        return "{0}for({1} = {2}; {1} < {3}; {1} += {4})\n{5}".format(
            tabs(indent),
            self.iterator_name,
            self.start,
            self.end,
            self.increment,
            self.next_operation.print(indent=indent + 1) if self.next_operation is not None else "")

    def cum_exec_time(self) -> float:
        t = 0
        for i in range(self.start, self.end):
            t += self.next_operation.cum_exec_time()

        return t

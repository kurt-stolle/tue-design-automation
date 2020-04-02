from abc import ABC
from typing import Union

from operations.operation import Operation, tabs
from operations.variable import Variable, Definition, Literal


class ForLoop(Operation, ABC):
    """A "For" Operation, assumes we only do int-based numerical for loops, e.g. from i=0 to i >= 10"""

    def __init__(self, start: Union[Definition,int], end: Union[Definition, int], increment: Union[Definition, int], iterator: Variable):
        # if start, end or increment is a literal (int) then convert it to an anonymous definition
        if isinstance(start, int):
            start = Literal(start)
        if isinstance(end, int):
            end = Literal(end)
        if isinstance(increment, int):
            increment = Literal(increment)

        # set public variables of the ForLoop
        self.iterator = iterator
        self.start = start
        self.end = end
        self.increment = increment

    def print_pseudo(self, indent=0) -> str:
        return "{0}for({1} = {2}; {1} < {3}; {1} += {4})\n{5}".format(
            tabs(indent),
            self.iterator.print_pseudo(),
            self.start.print_pseudo(),
            self.end.print_pseudo(),
            self.increment.print_pseudo(),
            self.next_operation.print_pseudo(indent=indent + 1) if self.next_operation is not None else "")

    def cum_exec_time(self) -> float:
        t = 0
        for i in range(self.start.value, self.end.value):
            t += self.next_operation.cum_exec_time()

        return t

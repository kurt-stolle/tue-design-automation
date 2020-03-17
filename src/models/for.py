from abc import ABC

from models.operation import Operation


class ForOperation(Operation, ABC):
    """A "For" Operation, assumes we only do int-based numerical for loops, e.g. from i=0 to i >= 10"""

    _exec_time = 10

    def __init__(self, start: int, end: int, increment: int):
        self.initOp = start
        self.checkOp = end
        self.increment = increment

    def print(self) -> str:
        return "for({}; {}; {})".format(self.initOp.print(), self.checkOp.print(), self.incrementOp.print())

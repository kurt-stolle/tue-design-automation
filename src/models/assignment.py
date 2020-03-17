from abc import ABC
from models.operation import Operation


class Equation(Operation, ABC):
    """An equation, e.g. A = B, or i < 10"""

    def __init__(self, name, equator="="):
        self.name = name
        self.equator = equator

    def print(self) -> str:
        return "{} {} {}".format(self.name, self.equator, self._nextOperation.print())

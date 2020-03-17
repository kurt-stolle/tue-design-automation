from abc import ABC

from models.operation import Operation


class LiteralValue(Operation, ABC):

    _exec_time = 0

    def __init__(self, v: str):
        self.v = v

    def print(self) -> str:
        return self.v
from operations.operation import Operation


class LiteralValue(Operation):

    _exec_time = 0

    def __init__(self, v: str):
        self.v = v

    def print(self, **kwargs) -> str:
        return self.v
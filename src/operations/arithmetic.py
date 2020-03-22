from operations import Operation


class Multiply(Operation):
    """A multiplication operation"""

    exec_time = 3

    def __init__(self):
        pass

    def print(self, **kwargs) -> str:
        assert self.next_operation is not None

        return " * " + self.next_operation.print(**kwargs)


class Add(Operation):
    """An addition operation"""

    exec_time = 2

    def __init__(self):
        pass

    def print(self, **kwargs) -> str:
        assert self.next_operation is not None

        return " + " + self.next_operation.print(**kwargs)

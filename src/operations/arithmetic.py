from operations import Operation


class Multiply(Operation):
    """A multiplication operation"""

    exec_time = 3

    def __init__(self):
        pass

    def print(self, **kwargs) -> str:
        assert self.nextOperation is not None

        return " * " + self.nextOperation.print(**kwargs)


class Add(Operation):
    """An addition operation"""

    exec_time = 2

    def __init__(self):
        pass

    def print(self, **kwargs) -> str:
        assert self.nextOperation is not None

        return " + " + self.nextOperation.print(**kwargs)

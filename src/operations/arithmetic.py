from operations import Operation


class Multiply(Operation):
    """A multiplication operation"""

    exec_time = 3

    def __init__(self):
        pass

    def print_pseudo(self, **kwargs) -> str:
        assert self.next_operation is not None

        return " * " + self.next_operation.print_pseudo(**kwargs)


class Add(Operation):
    """An addition operation"""

    exec_time = 2

    def __init__(self):
        pass

    def print_pseudo(self, **kwargs) -> str:
        assert self.next_operation is not None

        return " + " + self.next_operation.print_pseudo(**kwargs)

from operations.operation import Operation, tabs


class Assign(Operation):
    """Load the result of the next operation into the previous operation"""

    exec_time = 500

    def __init__(self, name):
        self.name = name

    def print(self, indent=0) -> str:
        return tabs(indent) + self.name + " = " + self.nextOperation.print(indent=indent) + ";"


class Fetch(Operation):
    """Fetches an operation from memory"""

    exec_time = 250

    def __init__(self, name: str):
        self.name = name

    def print(self, **kwargs) -> str:
        return self.name + (self.nextOperation.print(**kwargs) if self.nextOperation is not None else "")
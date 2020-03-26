class Variable:
    """Variable is used references a code variable with a name"""

    def __init__(self, name: str):
        self._name = name

    def print(self) -> str:
        return self._name

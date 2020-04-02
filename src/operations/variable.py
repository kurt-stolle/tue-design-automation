class Definition:
    """Definition is a compile-time definition used for readability, e.g. "#define name value" in C or "`name value" in
     Verilog"""

    def __init__(self, name: str, value: int):
        self._name = name.upper()
        self.value = value

    def print_pseudo(self) -> str:
        return self._name

    def print_verilog(self) -> str:
        return "`"+self._name

class Literal:
    """Literal is any literal (numerical) value"""
    def __init__(self, value: int):
        self._name = str(value)
        self.value = value

    def print_pseudo(self) -> str:
        return self._name

    def print_verilog(self)->str:
        return self._name

class Variable:
    """Variable references a code variable with a name"""

    def __init__(self, name: str):
        self._name = name

    def print_pseudo(self) -> str:
        return self._name

    def print_verilog(self) -> str:
        return self._name

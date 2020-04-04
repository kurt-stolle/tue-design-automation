class Definition:
    """Definition is a compile-time definition used for readability, e.g. "#define name value" in C or "`name value" in
     Verilog"""

    def __init__(self, name: str, value: int):
        self.name = name.upper()
        self.value = value

    def print_pseudo(self) -> str:
        return self.name

    def print_verilog(self) -> str:
        return "`" + self.name


class Literal:
    """Literal is any literal (numerical) value"""

    def __init__(self, value: int):
        self.name = str(value)
        self.value = value

    def print_pseudo(self) -> str:
        return self.name

    def print_verilog(self) -> str:
        return self.name


class Variable:
    """Variable references a code variable with a name"""

    def __init__(self, name: str, init: int = None):
        self.init = init
        self.name = name

    def print_pseudo(self) -> str:
        return self.name

    def print_verilog(self) -> str:
        return self.name


class Index(Variable):
    """Index a variable"""

    def __init__(self, var: Variable, idx: list):
        super().__init__(var.name)

        self.chain = idx

    # substitution in the chain, propagated from  Operation
    def sub(self, var_name: str, value: Literal):
        for k, v in enumerate(self.chain):
            try:
                if v.name == var_name:
                    self.chain[k] = value
                    return
            except AttributeError:
                pass

    def print_pseudo(self) -> str:
        idx = ""
        for v in self.chain:
            try:
                idx += v.print_pseudo()
            except AttributeError:
                idx += v

        return super().print_pseudo() + "[" + idx + "]"

    def print_verilog(self) -> str:
        idx = ""
        for v in self.chain:
            idx += v.print_verilog() if v.print_pseudo is not None else v

        return super().print_verilog() + "[" + "" + "]"

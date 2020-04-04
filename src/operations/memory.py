from operations.variable import Variable
from operations.operation import Operation, tabs


class Assign(Operation):
    """Load the result of the next operation into the previous operation"""

    exec_time = 4

    def __init__(self, var: Variable):
        self.var = var

    def print_pseudo(self, indent=0) -> str:
        return tabs(indent) + self.var.print_pseudo() + " = " + self.next_operation.print_pseudo(indent=indent)

    def print_verilog(self, **kwargs) -> str:
        return self.var.print_verilog() + " <= " + self.next_operation.print_verilog(**kwargs)


class Fetch(Operation):
    """Fetches an operation from memory"""

    exec_time = 2

    def __init__(self, var: Variable):
        self.var = var

    def print_pseudo(self, **kwargs) -> str:
        return self.var.print_pseudo() + self.next_operation.print_pseudo(**kwargs)

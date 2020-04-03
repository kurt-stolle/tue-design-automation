from operations.memory import *
from operations.forloop import *
from operations.operation import *
from operations.arithmetic import *
from operations.split import *
from operations.variable import *

_verilog_tpl = """

"""


class Root(Operation):
    """the Root operation performs initialization of the module"""

    _pseudo_tpl = """
Module({0}) {{
{1}
}}
    """

    _verilog_tpl = """
{0}

module Convolution (
	input clk,
	input rst,
	output reg done
);


    """

    def __init__(self, global_definitions=None):
        if global_definitions is None:
            global_definitions = []

        self.global_definitions = global_definitions

    def print_pseudo(self, **kwargs) -> str:
        globs = []
        for g in self.global_definitions:
            globs.append("{0} = {1}".format(g.print_pseudo(), g.value))

        return self._pseudo_tpl.format(', '.join(globs), self.next_operation.print_pseudo(**kwargs))

    def print_verilog(self, **kwargs) -> str:
        globs = []
        for g in self.global_definitions:
            globs.append("{0} {1}".format(g.print_verilog(), g.value))

        return self._verilog_tpl.format('\n'.join(globs))

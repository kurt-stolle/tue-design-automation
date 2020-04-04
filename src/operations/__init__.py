from operations.memory import *
from operations.forloop import *
from operations.operation import *
from operations.arithmetic import *
from operations.split import *
from operations.variable import *


class End(Operation):
	def __init__(self):
		pass

	def print_pseudo(self, **kwargs) -> str:
		return ""

	def print_verilog(selfs, **kwargs) -> str:
		return ""


class Root(Operation):
	"""the Root operation performs initialization of the module"""

	# PSEUDOCODE TEMPLATES
	_pseudo_tpl = """// Compile-time definitions
{0}

// Variable initialization
{1}

// Cross-correlation function
{2}"""

	# VERILOG TEMPLATES
	_verilog_tpl = """// Compile-time definitions
{}

// Module initialization
module Convolution (input clk,	input rst,	output reg done);

    // Adders
    {}
    
    // Multipliers
    {}
    
    // Variable initialization
    {}
    
    // Cross-correlation function 
    always @ (posedge clk) begin
		if(rst) begin
			enable <= 1'b0;
			{}
			done <= 1'b0;
		end
		else begin
		    {}
		end
	end
	
endmodule"""

	_verilog_mul_tpl = """
	wire [7:0] input_mul_{0}_I;
	wire [7:0] input_mul_{0}_K;
	wire [7:0] output_mul_{0};
	wire done_mul_{0};
	
	Multiplier mul_{0}(
		.clk(clk),
		.enable(enable),
		.input_I(input_mul_{0}_I),
		.input_K(input_mul_{0}_K),
		.output(output_mul_{0}),
		.done(done_mul_{0})
	);"""

	_verilog_add_tpl = """
	wire [7:0] input_add_{0}_I;
	wire [7:0] input_add_{0}_K;
	wire [7:0] output_add_{0};
	wire done_add_{0};
	
	Adder mul_{0}(
		.clk(clk),
		.enable(enable),
		.input_A(input_add_{0}_A),
		.input_B(input_add_{0}_B),
		.output(output_add_{0}),
		.done(done_add_{0})
	);"""

	def __init__(self, output_size: Definition, kernel_size: Definition, channels: Definition, filters: Definition):
		self.output_size = output_size
		self.kernel_size = kernel_size
		self.channels = channels
		self.filters = filters

	def ctime_vars(self):
		return [self.output_size, self.kernel_size, self.channels, self.filters]

	def vars(self):
		# if vars is called in the root operation, then  we also want to search and remove dumplicates
		res = self.next_operation.vars()
		names = []
		for k,v in enumerate(res):
			try:
				for n in names:
					if v.name == n:
						raise EOFError()

				names.append(v.name)
			except EOFError:
				del res[k]
				pass

		return res

	def count_multiplications(self):
		return self.count(lambda op: isinstance(op, Multiply))

	def count_additions(self):
		return self.count(lambda op: isinstance(op, Add))


	def print_pseudo(self, **kwargs) -> str:
		# compile-time variables, const statements
		globs = []
		for g in self.ctime_vars():
			globs.append("#define {0} {1};".format(g.print_pseudo(), g.value))
		globs = '\n'.join(globs)

		# variable initialization
		vars = []
		for v in self.vars():
			vars.append("int {0};".format(v.name))
		vars = '\n'.join(vars)

		# return pseudocode template
		return self._pseudo_tpl.format(
			globs,
			vars,
			self.next_operation.print_pseudo(**kwargs)
		)

	def print_verilog(self, **kwargs) -> str:
		# compile-time variables, const statements
		globs = []
		for g in self.ctime_vars():
			globs.append("{0} {1}".format(g.print_verilog(), g.value))

		globs = '\n'.join(globs)

		# adders
		adders = []
		for i in range(0, self.count_additions()):
			adders.append(self._verilog_add_tpl.format(i))
		adders = '\n\t'.join(adders)

		# multipliers
		multipliers = []
		for i in range(0, self.count_multiplications()):
			multipliers.append(self._verilog_mul_tpl.format(i))
		multipliers = '\n\t'.join(multipliers)

		# variable initialization
		vars_init = []
		vars_reset = []
		for v in self.vars():
			vars_init.append("reg [7:0] {};".format(v.name))
			vars_reset.append("{} <= 0;".format(v.name))

		vars_init = '\n\t'.join(vars_init)
		vars_reset = '\n\t\t\t'.join(vars_reset)

		# return verilog template
		return self._verilog_tpl.format(
			globs,
			adders,
			multipliers,
			vars_init,
			vars_reset,
			self.next_operation.print_verilog()
		)

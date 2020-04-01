`timescale 1ns / 1ps
module Convolution_tb;

	// Inputs
	reg clk;
	reg rst;

	// Outputs
	
	wire done;

	// Instantiate the Unit Under Test (UUT)
	Convolution uut (
		.clk(clk),
		.rst(rst),
		.done(done)	
		//.maxPoolingDone(maxPoolingDone)	
	);
	
	initial begin
		clk = 0;
		rst = 1;
		#10;
		rst = 0;
	end
	
	always #5 clk = ~clk;

	initial
     		$monitor("At time %t, value = %h (%0d)",$time, done, done);
endmodule
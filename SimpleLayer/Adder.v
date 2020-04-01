/*
	Author: Aniket Badhan
	Description: Addition stage 2 of Convolution with Laplacian filter
*/

module Adder(
	input [7:0] input1,
	input [7:0] input2,
    output reg [8:0] output1,
	input clk,
	input enable,
	output reg done
    );
	
	always @ (posedge clk) begin
		if(enable) begin	
			output1 <= {1'b0, input1} + {1'b0, input2};
			done <= 1'b1;
		end
		else begin
			output1 <= 0;
			done <= 1'b0;
		end
	end
	
endmodule

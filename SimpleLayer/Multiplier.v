module Multiplier(
	input clk,
	input enable,
	input [3:0] input_I,
	input [3:0] input_K,
	output reg [7:0] output1,
	output reg done
    );
	
	always @ (posedge clk) begin
		if(enable) begin
			output1 <= input_I * input_K;
			done <= 1'b1;
		end
		else begin
			output1 <= 0;
			done <= 1'b0;
		end

	end
		
endmodule

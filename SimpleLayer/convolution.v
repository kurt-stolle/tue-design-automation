`define IMAGEROW	128
`define IMAGECOL	128
`define IMAGEDIM	3
`define CONVROW		32
`define CONVCOL		32
`define CONVDIM		8
`define KERNELROW	8
`define KERNELCOL	8

module Convolution (
	input clk,
	input rst,
	output reg done
);

	reg [7:0] imageArray [0:`IMAGEROW*`IMAGECOL-1];				//memory buffer for storing image and the convolution of it with the laplacian filter
	reg [7:0] kernelArray [0:`KERNELROW*`KERNELCOL-1];		
	reg [21:0] Output [0:`CONVROW*`CONVCOL-1];	
	
	initial $readmemb("image1.txt", imageArray, 0, `IMAGEROW*`IMAGECOL-1);	//reading image
	initial $readmemb("kernel.txt", kernelArray, 0, `KERNELROW*`KERNELCOL-1);	//reading image
	

	//internal signals for the Convolution of Image with the laplacian filter
	wire [3:0] input1_image;
	wire [3:0] input1_kernel;
	wire [3:0] input2_image;
	wire [3:0] input2_kernel;
	wire [7:0] tempOutput1_image;
	wire [7:0] tempOutput2_image;
	wire [8:0] output_image;
	
	reg enable;
	wire done1_image;
	wire done2_image;
	wire done3_image;

	reg [14:0] writeCount_image;
	reg [14:0] colCount_image;
	reg [6:0] rowCount_image;
	
	Multiplier m1_image(
		.clk(clk),
		.enable(enable),
		.input_I(input1_image),
		.input_K(input1_kernel),
		.output1(tempOutput1_image),
		.done(done1_image)
	);
	
	Multiplier m2_image(
		.clk(clk),
		.enable(enable),
		.input_I(input2_image),
		.input_K(input2_kernel),
		.output1(tempOutput2_image),
		.done(done2_image)
	);

	Adder add1_image(
		.clk(clk),
		.enable(done1_image&done2_image),
		.input1(tempOutput1_image),
		.input2(tempOutput2_image),
		.output1(output_image),
		.done(done3_image)
	);

	
	// //assigning values to the input signals for the convolution of image with the laplcian filter
	assign input1_image = (enable && (rowCount_image <= `IMAGEROW )) ? imageArray[rowCount_image * `IMAGECOL + colCount_image][3:0] : 4'b0000;
	assign input1_kernel = (enable && (rowCount_image <= `IMAGEROW)) ? imageArray[rowCount_image * `IMAGECOL + colCount_image][3:0] : 4'b0000;
	assign input2_image = (enable && (rowCount_image <= `IMAGEROW)) ? imageArray[rowCount_image * `IMAGECOL + colCount_image][3:0] : 4'b0000;
	assign input2_kernel = (enable && (rowCount_image <= `IMAGEROW)) ? imageArray[rowCount_image * `IMAGECOL + colCount_image][3:0] : 4'b0000;
	
	always @ (posedge clk) begin
		if(rst) begin
			enable <= 1'b0;
			colCount_image <= 0;
			rowCount_image <= 0;
			writeCount_image <= 0;
			done <= 1'b0;
		end
		else begin
			enable <= 1'b1;
			if(enable) begin												//Once the enable_stage1_image is high, start generating the count_stage1_image values for creating the input values to ConvolutionStage1 module for image convolution
				if(rowCount_image <= `IMAGEROW ) begin
					if(colCount_image <= `IMAGECOL) begin
						colCount_image <= colCount_image + 1'b1; 
						rowCount_image <= rowCount_image;
					end
					else begin
						colCount_image <= 0;
						rowCount_image <= rowCount_image + 1'b1;
					end
				end
				else begin
					colCount_image <= colCount_image;
					rowCount_image <= rowCount_image;
				end
			end
			else begin
				colCount_image <= 0;
				rowCount_image <= 7'b0000001;
			end
		end
		if(done3_image) begin
			if(writeCount_image < `CONVCOL*`CONVROW) begin
				Output[writeCount_image] <= output_image;
				writeCount_image <= writeCount_image + 1'b1;
			end
			else begin
				writeCount_image <= writeCount_image;
				done <= 1'b1;
			end
		end
		//start writing the output of convolution to the memory buffer once the done signal from the last stage of addition arrives
		else begin
			writeCount_image <= writeCount_image;
		end
	end	

endmodule

# Electronic Design Automation Project 

This repository accompanies our solution for the course Electronic Design Automation (5SIB0) at Eindhoven University of Technology. 

## Usage

The design automation tool synthesises a Verilog implementation of a cross-correlation function for a convolutional layer in a neural network. It does this based on parameters supplied by the user:
- `input_size`: The size (width and height) of the input matrix
- `channels`: The amount of input channels (e.g. 3 for an RGB input "image")
- `kernel_size`: The size (width and height) of the convolution kernel
- `filters`: The amount of convoliton sets, i.e. the amount dimentions on the output

## Modules

The solution consists of following modules (see the `src` directory):
- `cmd`: the entrypoint of the script which performs the optimization algorithm
- `operations`: contains all `Operation` subclasses, used to make an abstract representation of the cross-correlation loop
- `generator`: generates an abstract representation of the network and performs the loop unrolling optimization


## Autors

K.H.W. Stolle <k.h.w.stolle@student.tue.nl>
M. van Dijke <m.v.dijke@student.tue.nl>
S.L. Kamp <s.l.kamp@student.tue.nl>

#!/usr/bin/env python

import generator


def generate(input_size: int = 32, channels: int = 3, kernel_size: int = 3, filters: int = 8):
    # Start with our starting point: a new implementation based on our parameters
    impl = generator.new_implementation(input_size, channels, kernel_size,
                                        filters)

    print("Starting synthesis algorithm")

    print("\n-- Iteration 0 --")
    print("Cost: {0}".format(impl.cum_exec_time()))
    print("Pseudo code:\n{0}".format(impl.print_pseudo(indent=1)))
    print("Verilog code:\n{0}".format(impl.print_verilog()))

    # Keep iterating until we can no longer unroll due to hardware limitations
    for i in range(1, 3):
        new_impl = generator.optim_loop_unroll(impl)

        print("\n-- Iteration {} --".format(i))
        print("Cost: {0}".format(new_impl.cum_exec_time()))
        print("Pseudo code:\n{0}".format(new_impl.print_pseudo(indent=1)))
        print("Verilog code:\n{0}".format(new_impl.print_verilog()))

        # Check whether the new implementation works on the current hardware
        if False:
            pass

        # Set the current implementation to the new implementation we just created
        impl = new_impl

    exit(0)

if __name__ == "__main__":
    generate()

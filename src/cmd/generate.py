#!/usr/bin/env python

import cli.log
import generator
import operations


@cli.log.LoggingApp
def generate(app):
    try:
        print("starting generation with params: ", app.params)

    # Start with our starting point: a new implementation based on our parameters
        impl = generator.new_implementation(app.params.input_size, app.params.kernel_size)

        print("CURRENT COST: {0}".format(impl.cum_exec_time()))
        print("ITERATION 0:\n{0}".format(impl.print(indent=1)))

        # Test the unroll function by running it on the first operation in the chain, which we know is the subclass
        # operations.ForLoop
        inner_loop, inner_loop_parent = generator.find_inner_loop(impl)  # impl starts with a chain of ForLoop

        print("Inner loop {0}".format(inner_loop))

        unrolled_loop = generator.loop_unroll(inner_loop)

        inner_loop_parent.nextOperation = unrolled_loop  # Replace the body of the parent loop with an unrolled version

        print("CURRENT COST: {0}".format(impl.cum_exec_time()))
        print("ITERATION 1:\n{0}".format(impl.print(indent=1)))

    except Exception as e:
        print(e)
        exit(1)

    exit(0)


generate.add_param("-f", "--fpga-model", help="the fpga model", default="default", type=str)
generate.add_param("-i", "--input-size", help="the convolution layer input size", default=32, type=int)
generate.add_param("-k", "--kernel_size", help="the convolution kernel size", default=5, type=int)

if __name__ == "__main__":
    generate.run()

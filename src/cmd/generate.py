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

        # Keep iterating until we can no longer unroll due to hardware limitations
        for i in range(1, 3):
            new_impl = generator.optim_loop_unroll(impl)

            print("CURRENT COST: {0}".format(new_impl.cum_exec_time()))
            print("ITERATION {1}:\n{0}".format(new_impl.print(indent=1), i))

            # Check whether the new implementation works on the current hardware
            if False:
                pass

            # Set the current implementation to the new implementation we just created
            impl = new_impl

    except Exception as e:
        print(e)
        exit(1)

    exit(0)


generate.add_param("-f", "--fpga-model", help="the fpga model", default="default", type=str)
generate.add_param("-i", "--input-size", help="the convolution layer input size", default=32, type=int)
generate.add_param("-k", "--kernel_size", help="the convolution kernel size", default=5, type=int)

if __name__ == "__main__":
    generate.run()

#!/usr/bin/env python
import argparse

import generator
import operations

dbg_markdown = """
---------------------------------------------------------------------------
# Iteration {}
- Cost:            {}
- Memory accesses: {}
- Concurrency:     {}

C-Style Pseudocode
```
{}
```

Verilog
```
{}
```"""


def print_implementation(i: int, impl: operations.Root, print_verilog: bool, print_pseudo: bool):
    print(dbg_markdown.format(
        i,
        impl.cum_exec_time(),
        impl.count(lambda op: isinstance(op, operations.Assign) or isinstance(op, operations.Fetch)),
        impl.count_multiplications()+impl.count_additions(),
        impl.print_pseudo() if print_pseudo else "DISABLED",
        impl.print_verilog() if print_verilog else "DISABLED"
    ))


def generate(input_size: int = 32, channels: int = 3, kernel_size: int = 3, filters: int = 8,
             available_concurrency: int = 100, print_verilog: bool = False, print_pseudo: bool = False):
    # Start with our starting point: a new implementation based on our parameters
    impl = generator.new_implementation(input_size, channels, kernel_size,
                                        filters)

    print("Starting synthesis algorithm")

    print_implementation(0, impl, print_verilog, print_pseudo)

    # Keep iterating until we can no longer unroll due to hardware limitations
    for i in range(1, 4):
        new_impl = generator.optim_loop_unroll(impl)  # unroll loops

        print_implementation(i, new_impl, print_verilog, print_pseudo)  # output the current implementation

        # Check whether the new implementation works on the current hardware
        # if impl.count(lambda op: isinstance(op, operations.Assign) or isinstance(op, operations.Fetch)) > available_concurrency:
        #     return

        # Set the current implementation to the new implementation we just created
        impl = new_impl


def get_args():
    parser = argparse.ArgumentParser(description='Generate the verilog implementation',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', "--input", metavar="INPUT_SIZE", type=int, required=True)
    parser.add_argument('-c', "--channels", metavar="CHANNELS", type=int, default=3)
    parser.add_argument('-k', '--kernel', metavar='KERNEL_SIZE', type=int, default=3,
                        help='Size (width and height) of the convolution kernel')
    parser.add_argument('-f', '--filters', metavar='FILTERS', type=int, default=8,
                        help='Batch size')
    parser.add_argument('-a', '--concurrency', metavar='AVAILABLE_CONCURRENCY', type=int, default=100,
                        help='Available concurrency')

    return parser.parse_args()


import timeit
if __name__ == "__main__":
    args = get_args()

    print(timeit.timeit(
        lambda: generate(args.input, args.channels, args.kernel, args.filters, args.concurrency, print_verilog=True, print_pseudo=True),
        number=1
    ))

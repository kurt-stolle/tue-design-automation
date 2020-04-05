#!/usr/bin/env python

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
        if False:
            pass

        # Set the current implementation to the new implementation we just created
        impl = new_impl

import timeit
if __name__ == "__main__":
    print(timeit.timeit(
        lambda: generate(16, channels=3, kernel_size=3, filters=16, available_concurrency=200, print_verilog=False, print_pseudo=True),
        number=1
    ))

import operations


def new_implementation(input_size: int,
                       kernel_size: int,
                       channels: int = 4,
                       filters: int = 7,
                       stride: int = 1) -> operations.Operation:
    """Create a new convolution (cross-correlation) loop in the most basic form. Essentially, this is the starting
    point of any generator."""



    # Todo implement the stride
    if stride != 1:
        raise AssertionError("stride must be equal to 1 (other values not yet implemented)")

    # The kernel size must be an odd number (1, 3, etc)
    assert (kernel_size % 2) == 1

    # Define the variables
    var_n_filter = operations.Variable("n_filter")
    var_S_row = operations.Variable("S_row")
    var_S_col = operations.Variable("S_col")
    var_I_chan = operations.Variable("I_chan")
    var_K_row = operations.Variable("K_row")
    var_K_col = operations.Variable("K_col")

    # Define definitions
    # We assume that we don't need to add any padding (if padding is desired, then the data should be pre-padded before
    # going into our system. The output size is thus: output_size = (input_size-kernel_size)/stride + 2
    def_output_size = operations.Definition("output_size", int((input_size - kernel_size) / stride + 1))
    def_kernel_size = operations.Definition("kernel_size", kernel_size)
    def_channels = operations.Definition("channels", channels)
    def_filters = operations.Definition("filters", filters)

    # Define a root operation which will be the result of this method
    root_operation = operations.Root([
        def_output_size,
        def_kernel_size,
        def_channels,
        def_filters
    ])

    # Define our loops
    loop_n_filters = operations.ForLoop(0, def_filters, 1, iterator=var_n_filter)
    loop_output_rows = operations.ForLoop(0, def_output_size, 1, iterator=var_S_row)
    loop_output_cols = operations.ForLoop(0, def_output_size, 1, iterator=var_S_col)
    loop_input_chan = operations.ForLoop(0, def_channels, 1, iterator=var_I_chan)
    loop_kernel_rows = operations.ForLoop(0, def_kernel_size, 1, iterator=var_K_row)
    loop_kernel_cols = operations.ForLoop(0, def_kernel_size, 1, iterator=var_K_col)

    # Add our newly created loops to the body of the root_operation in sequence
    root_operation.then(
        loop_output_rows.then(
            loop_output_cols.then(
                loop_n_filters.then(
                    loop_input_chan.then(
                        loop_kernel_rows.then(
                            loop_kernel_cols
                        )
                    )
                )
            )
        )
    )

    # Define the assignment operation - even though this is a matrix assignment,
    # we neglect the lookup times for the arrays
    s_cur = "S[n_filter][S_row][S_col]"

    assign_matrix_element = operations.Assign(s_cur).then(
        operations.Fetch(s_cur).then(
            operations.Add().then(
                operations.Fetch("I[I_chan][S_row+K_row][S_col+K_col]").then(
                    operations.Multiply().then(
                        operations.Fetch("K[K_row][K_col]")
                    )
                )
            )
        )
    )

    # Add the assignment opration after the inner loop
    loop_kernel_cols.then(assign_matrix_element)

    # Define the multiplication operation

    return root_operation

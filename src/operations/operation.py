def tabs(n: int):
    t = ""
    for i in range(n):
        t += "  "

    return t


class Operation(object):
    """An operation, e.g. "For", "Assign" and "Multiply". This essentially creates a way of "functionally
    programming" the for-loop of the CNN, making optimization easier"""

    nextOperation = None  # the next operation in the chain
    exec_time = 1

    def print(self, **kwargs) -> str:
        if self.nextOperation is not None:
            return self.nextOperation.print(**kwargs)
        else:
            raise ValueError("cannot print an empty operations chain")


    def cum_exec_time(self) -> float:
        """quantify the cumulative performance of this operation and it's next operations, allowing for optimization.

        :returns memory used, execution time"""

        return self.exec_time + (self.nextOperation.cum_exec_time() if self.nextOperation is not None else 0)

    def then(self, nextOperation: any):
        """set the next operation to be performed after this operation is done"""
        self.nextOperation = nextOperation

        return self


from __future__ import annotations  # The operation class's annotations reference itself

from typing import List

from operations.variable import *


def tabs(n: int):
    """returns n amount of 'tabs' (two spaces) for readability of the output"""
    t = ""
    for i in range(n):
        t += "  "

    return t


class Operation(object):
    """An operation, e.g. "For", "Assign" and "Multiply". This essentially creates a way of "functionally
    programming" the for-loop of the CNN, making optimization easier"""

    next_operation: Operation = None  # the next operation in the chain
    prev_operation: Operation = None  # the previous operation in the chain

    exec_time = 0

    def print_pseudo(self, **kwargs) -> str:
        raise NotImplementedError("cannot execute print_pseudo on the Operation class: a child class must define this method")

    def print_verilog(selfs, **kwargs) -> str:
        raise NotImplementedError("cannot execute print_verilog on the Operation class: a child class must define this method")

    def walk(self):
        """walk the chain of  operations in the next-direction"""
        cursor = self.next_operation
        while cursor is not None:
            yield cursor
            cursor = cursor.next_operation

    def count(self, fn) -> int:
        """count how many times an assertion can be made about the class in a chain of operations"""
        ass = fn(self)

        if self.next_operation is not None:
            return (1 if ass else 0) + self.next_operation.count(fn)

        return 1 if ass else 0

    # Substitution
    def sub(self, var_name: str, value: Literal):
        """Substitute a Variable for a Literal"""
        try:
            if self.var.name == var_name:
                self.var = value
                return

            # A var may have a sub method too, like for Index. Make sure we propagate fully
            self.var.sub(var_name, value)
        except AttributeError:
            pass

        if self.next_operation is not None:
            self.next_operation.sub(var_name, value)

    # Find all variables - all are supposed global
    def vars(self) -> List[Variable]:
        """collect a list of all Variables in the list"""
        l = []

        try:
            if isinstance(self.var, Index):
                l.append(self.var.var)
            if isinstance(self.var, Variable):
                l.append(self.var)
        except AttributeError:
            pass

        if self.next_operation is not None:
            next = self.next_operation.vars()
            l.extend(next)

        return l

    def cum_exec_time(self) -> float:
        """quantify the cumulative performance of this operation and it's next operations, allowing for optimization.

        :returns memory used, execution time"""

        return self.exec_time + (self.next_operation.cum_exec_time() if self.next_operation is not None else 0)

    def then(self, next_operation: Operation) -> Operation:
        """set the next operation to be performed after this operation is done"""

        # Double link
        self.next_operation = next_operation
        next_operation.prev_operation = self

        return self



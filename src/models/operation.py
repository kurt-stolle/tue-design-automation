from abc import ABCMeta, abstractmethod, abstractproperty


class Operation(object):
    """An operation, e.g. "For", "Assign" and "Multiply". This essentially creates a way of "functionally
    programming" the for-loop of the CNN, making optimization easier"""

    __metaclass__ = ABCMeta

    _nextOperation = None  # the next operation in the chain

    @property
    @abstractmethod
    def exec_time(self) -> float:
        """The execution time of this operation"""
        pass

    @abstractmethod
    def print(self) -> str:
        """print the operation."""
        pass

    @classmethod
    def cum_exec_time(cls) -> (float, float):
        """quantify the cumulative performance of this operation and it's next operations, allowing for optimization.

        :returns memory used, execution time"""

        return cls._executionTime, cls._nextOperation.benchExecutionTime()

    @classmethod
    def then(cls, _next):
        """set the next operation to be performed after this operation is done"""
        cls._nextOperation = _next

        return next

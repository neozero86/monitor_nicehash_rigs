from Main.strategy.operation_status import OperationStatus
from Main.singleton import Singleton

class Error(OperationStatus):
    def __init__(self, max_count=-1):
        super(Error, self).__init__(max_count)
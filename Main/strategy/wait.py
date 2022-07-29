from Main.strategy.operation_status import OperationStatus
from Main.singleton import Singleton

class Wait(OperationStatus):
    def __init__(self, max_count):
        super(Wait, self).__init__(max_count)
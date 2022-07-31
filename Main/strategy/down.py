from Main.strategy.operation_status import OperationStatus
from Main.singleton import Singleton

class Down(OperationStatus):
    def __init__(self, max_count=0):
        super(Down, self).__init__(max_count)

    def should_wait(self):
        return True

    def is_down(self):
        return True
from Main.operational_status.operation_status import OperationStatus
from Main.singleton import Singleton

class Normal(OperationStatus):
    def __init__(self, max_count = 1):
        super(Normal, self).__init__(max_count)

    def is_ok(self):
        return True
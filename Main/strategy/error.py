from Main.strategy.operation_status import OperationStatus

class Error(OperationStatus):
    def __init__(self, max_count):
        super(Error, self).__init__(max_count)
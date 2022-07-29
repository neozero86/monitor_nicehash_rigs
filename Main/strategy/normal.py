from Main.strategy.operation_status import OperationStatus

class Normal(OperationStatus):
    def __init__(self, max_count):
        super(Normal, self).__init__(max_count)
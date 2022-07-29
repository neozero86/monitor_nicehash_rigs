from Main.strategy.operation_status import OperationStatus

class Down(OperationStatus):
    def __init__(self, max_count):
        super(Down, self).__init__(max_count)
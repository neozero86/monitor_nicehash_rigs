from Main.strategy.operation_status import OperationStatus

class Wait(OperationStatus):
    def __init__(self, max_count):
        super(Wait, self).__init__(max_count)
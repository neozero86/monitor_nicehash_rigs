class OperationStatus():
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0

    def should_wait(self):
        
        return self.count < self.max_count

    


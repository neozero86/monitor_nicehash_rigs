from Main.singleton import Singleton

class OperationStatus():
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0

    def update(self):
        self.count += 1

    def should_wait(self):
        return self.count < self.max_count
    
    def is_ok(self):
        return False

    def is_down(self):
        return False
    
    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, OperationStatus):
            return self.__class__ == other.__class__ and self.count == other.count and self.max_count == other.max_count
        return False

    def __hash__(self):
        return hash(self.__class__) + hash(self.count) + hash(self.max_count)

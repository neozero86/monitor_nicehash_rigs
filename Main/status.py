from enum import Enum

class Status(Enum):
    ACTIVE = True
    MINING = True
    INACTIVE = False
    STOPPED = False
    OFFLINE = False
    ERROR = False
    UNKNOWN = False
    
    @staticmethod
    def from_str(text):
        statuses = [status for status in dir(
            Status) if not status.startswith('_')]
        if text in statuses:
            return getattr(Status, text)
        return None
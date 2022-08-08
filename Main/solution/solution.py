class Solution():
    
    def __init__(self):
        pass

    def next_status(self):
        pass

    def solve(self, api, rig_id, email_sender, problem, logger):
        pass

    def __eq__(self, other):
        if isinstance(other, Solution):
            return self.__class__ == other.__class__
        return False
            
    def __hash__(self):
        return hash(self.__class__)

    def pretty_print(self):
        return type(self).__name__
class Solution():
    
    def __init__(self):
        pass

    def next_status(self):
        pass

    def solve(self, api, rig_id, rig_name, email_sender, problem, logger):
        pass

    def __eq__(self, other):
        if isinstance(other, Solution):
            return self.__class__ == other.__class__
        return False
            
    def __hash__(self):
        return hash(self.__class__)

    def pretty_print(self):
        return type(self).__name__

    def __str__(self):
        return self.pretty_print()

    def __repr__(self):
        return self.__str__()
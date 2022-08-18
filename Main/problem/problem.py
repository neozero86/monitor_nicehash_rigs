from Main.solution.human import Human
from Main.solution.restart_rig import RestartRig
from Main.solution.restart_worker import RestartWorker
from Main.solution.start_worker import StartWorker


class Problem:
    def __init__(self, message):
        self.message = message

    def solutions(self):
        return [RestartWorker(),RestartRig(),StartWorker(),Human()]

    def severity(self):
        return 1

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Problem):
            return self.message == other.message
        return False

    def __hash__(self):
        return hash(self.message)

    def pretty_print(self):
        return type(self).__name__

    def match(self, problem_name):
        return self.pretty_print() == problem_name
            
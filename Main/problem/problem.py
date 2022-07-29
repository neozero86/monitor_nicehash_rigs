from Main.solution.human import Human
from Main.solution.restart_rig import RestartRig
from Main.solution.restart_worker import RestartWorker


class Problem:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()

    def solutions(self):
        return [RestartWorker(),RestartRig(),Human()]

    def severity(self):
        return 1
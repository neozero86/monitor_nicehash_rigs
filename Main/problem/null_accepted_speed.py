from Main.problem.problem import Problem

class NullAcceptedSpeed(Problem):
    def __init__(self, rig_name):
        super(NullAcceptedSpeed, self).__init__('[{}] speedAccepted = 0.'.format(rig_name))

    def severity(self):
        return 3
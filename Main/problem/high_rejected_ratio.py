from Main.problem.problem import Problem

class HighRejectedRatio(Problem):
    def __init__(self, rig_name, rejected_ratio):
        super(HighRejectedRatio, self).__init__('[{}] rejected_ratio = {}%.'.format(rig_name,rejected_ratio*100))
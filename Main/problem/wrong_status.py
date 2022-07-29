from Main.problem.problem import Problem

class WrongStatus(Problem):
    def __init__(self, rig_name, device_name, device_id, status):
        super(WrongStatus, self).__init__('[{}.{}.{}] current status is {}.'.format(rig_name, device_name, device_id, status))

    def severity(self):
        return 7
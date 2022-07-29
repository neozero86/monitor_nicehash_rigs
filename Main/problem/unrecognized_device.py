from Main.problem.problem import Problem

class UnrecognizedDevice(Problem):
    def __init__(self, rig_name, device_name):
        super(UnrecognizedDevice, self).__init__('[{}.{}] device not recognized, check DEVICES variable in conf.json'.format(rig_name, device_name))

    def severity(self):
        return 7
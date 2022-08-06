from Main.problem.problem import Problem

class DeviceCountError(Problem):
    def __init__(self, rig_name, expected_devices_count, devices_count):
        super(DeviceCountError, self).__init__('[{}] has only {} devices. The expected amount is {}'.format(rig_name,devices_count,expected_devices_count))

    def severity(self):
        return 4
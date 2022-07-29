

class WrongStatus(Problem):
    def __init__(self, rig_name, device_name, status):
        super(WrongStatus, self).__init__('[{}.{}] current status is {}.'.format(rig_name, name, status))
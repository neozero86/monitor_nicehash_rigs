

class HostDown(Problem):
    def __init__(self, rig_name):
        super(HostDown, self).__init__('[{}] host is down.'.format(rig_name))
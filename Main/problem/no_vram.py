from Main.problem.problem import Problem

class NoVram(Problem):
    def __init__(self, rig_name, device_name, device_id):
        super(NoVram, self).__init__('[{}.{}.{}] no vram metric'.format(rig_name, device_name, device_id))

    def severity(self):
        return 2
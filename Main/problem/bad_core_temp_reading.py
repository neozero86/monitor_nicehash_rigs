from Main.problem.problem import Problem

class BadCoreTempReading(Problem):
    def __init__(self, rig_name, device_name, device_id):
        super(BadCoreTempReading, self).__init__('[{}.{}.{}] bad core temp reading'.format(rig_name, device_name, device_id))

    def severity(self):
        return 3
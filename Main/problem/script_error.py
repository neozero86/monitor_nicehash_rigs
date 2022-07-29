from Main.problem.problem import Problem

class ScriptError(Problem):
    def __init__(self, rig_name, exception):
        super(ScriptError, self).__init__('Rig: {}; Script error [{}]'.format(rig_name, str(exception)))
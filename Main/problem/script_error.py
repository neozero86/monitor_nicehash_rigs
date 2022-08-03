from Main.problem.problem import Problem
import traceback

class ScriptError(Problem):
    def __init__(self, rig_name, exception):
        text = '\n'.join(traceback.format_exception(None, value=exception, tb=exception.__traceback__))
        super(ScriptError, self).__init__('Rig: {}; Script error [{}]'.format(rig_name, text))

    def severity(self):
        return 6
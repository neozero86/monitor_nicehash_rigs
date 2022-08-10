from Main.problem.metric_exceeded_superior_limit import MetricExceededSuperiorLimit
from Main.solution.human import Human
from Main.solution.restart_rig import RestartRig
from Main.solution.restart_worker import RestartWorker
from Main.solution.stop_worker import StopWorker

class HighTemp(MetricExceededSuperiorLimit):
    def __init__(self, rig_name, device_name, device_id, metric_name, metric, limit_metric):
        super(HighTemp, self).__init__(rig_name, device_name, device_id, metric_name + " temp", metric, limit_metric)

    def severity(self):
        return 6

    def solutions(self):
        return [RestartWorker(),RestartRig(),StopWorker(),Human()]

from Main.problem.metric_exceeded_superior_limit import MetricExceededSuperiorLimit

class HighCoreTemp(MetricExceededSuperiorLimit):
    def __init__(self, rig_name, device_name, device_id, metric_name, metric, limit_metric):
        super(HighCoreTemp, self).__init__(rig_name, device_name, device_id, metric_name, metric, limit_metric)

    def severity(self):
        return 6
from Main.problem.metric_exceeded_inferior_limit import MetricExceededInferiorLimit

class LowHashRate(MetricExceededInferiorLimit):
    def __init__(self, rig_name, device_name, device_id, metric_name, metric, limit_metric):
        super(LowHashRate, self).__init__(rig_name, device_name, device_id, metric_name, metric, limit_metric)

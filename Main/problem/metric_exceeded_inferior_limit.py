from Main.problem.metric_exceeded import MetricExceeded

class MetricExceededInferiorLimit(MetricExceeded):
    def __init__(self, rig_name, device_name, device_id, metric_name, metric, limit_metric):
        super(MetricExceededInferiorLimit, self).__init__(rig_name, device_name, device_id, metric_name, metric, limit_metric)

    def sign_message(self):
        return "lower than min"
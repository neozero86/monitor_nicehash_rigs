from Main.problem.metric_exceeded import MetricExceeded

class MetricExceededSuperiorLimit(MetricExceeded):
    def __init__(self, rig_name, device_name, device_id, metric_name, metric, limit_metric):
        super(MetricExceededSuperiorLimit, self).__init__(rig_name, device_name, device_id, metric_name, metric, limit_metric)

    def sign_message(self):
        return "exceed max"
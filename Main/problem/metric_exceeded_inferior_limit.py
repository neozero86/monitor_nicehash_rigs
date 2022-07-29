

class MetricExceededInferiorLimit(Problem):
    def __init__(self, rig_name, device_name, metric_name, metric, limit_metric):
        super(MetricExceededInferiorLimit, self).__init__(rig_name, device_name, metric_name, metric, limit_metric)

    def sign_message():
        return "lower than min"


class MetricExceededSuperiorLimit(Problem):
    def __init__(self, rig_name, device_name, metric_name, metric, limit_metric):
        super(MetricExceededSuperiorLimit, self).__init__(rig_name, device_name, metric_name, metric, limit_metric)

    def sign_message():
        return "exceed max"
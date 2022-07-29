from Main.problem.problem import Problem

class MetricExceeded(Problem):
    def __init__(self, rig_name, device_name, device_id, metric_name, metric, limit_metric):
        super(MetricExceeded, self).__init__('[{}.{}.{}] current {}: {} {} {} {}.'.format(rig_name, device_name, device_id, metric_name, metric, self.sign_message(), metric_name, limit_metric))

    def sign_message(self):
        pass

    def severity(self):
        return 4
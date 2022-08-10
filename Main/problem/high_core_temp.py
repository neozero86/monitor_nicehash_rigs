from Main.problem.high_temp import HighTemp


class HighCoreTemp(HighTemp):
    def __init__(self, rig_name, device_name, device_id, metric, limit_metric):
        super(HighCoreTemp, self).__init__(rig_name, device_name, device_id, "core", metric, limit_metric)
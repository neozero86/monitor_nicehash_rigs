from Main.problem.high_temp import HighTemp

class HighVRamTemp(HighTemp):
    def __init__(self, rig_name, device_name, device_id, metric, limit_metric):
        super(HighVRamTemp, self).__init__(rig_name, device_name, device_id, "VRam", metric, limit_metric)
from Main.problem.metric_exceeded_inferior_limit import MetricExceededInferiorLimit
from Main.problem.metric_exceeded_superior_limit import MetricExceededSuperiorLimit
from Main.problem.no_vram import NoVram
from Main.problem.unrecognized_device import UnrecognizedDevice
from Main.problem.wrong_status import WrongStatus
from Main.status import Status
from Main.api.api_result_constants import *

class Device():
    def __init__(self, id, name, rig, status=Status.ACTIVE):
        self.id = id
        self.name = name
        self.rig = rig
        self.status = status
        self.thresholds = None
        self.power = 0
        self.hr = 0
        self.fan_speed = 0
        self.temp_encoded = 0
        self.core_temp = 0
        self.hot_spot_temp = 0
        self.vram_temp = 0

    def set_threshold(self, device_stats):
        for dev_id, values in device_stats.items():
            if (dev_id in self.name):
                self.thresholds = values
                break

    def update(self, actual_info):
        self.power = actual_info[POWER]
        self.hr = actual_info[HR]
        self.fan_speed = actual_info[FAN_SPEED]
        self.temp_encoded = actual_info[TEMP_ENCODED]
        self.core_temp = actual_info[CORE_TEMP]
        self.hot_spot_temp = actual_info[HOT_SPOT_TEMP]
        self.vram_temp = actual_info[VRAM_TEMP]
        self.status = actual_info[STATUS]

    def check(self):
        errors=[]
        if (not self.thresholds):
            errors.append(UnrecognizedDevice(self.rig.name, 'device [{}] not recognized'.format(self.name)))
            return errors
        if(not self.status.value):
            errors.append(WrongStatus(self.rig.name, self.name, self.id, self.status.name))
        if(self.vram_temp==-1):
            errors.append(NoVram(self.rig.name, self.name, self.id))
        elif(self.vram_temp>self.thresholds.max_vram_temp):
            errors.append(MetricExceededSuperiorLimit(self.rig.name, self.name, self.id, "vram_temp", self.vram_temp, self.thresholds.max_vram_temp))
        if(self.power>self.thresholds.max_power):
            errors.append(MetricExceededSuperiorLimit(self.rig.name, self.name, self.id, "power", self.power, self.thresholds.max_power))
        if(self.temp_encoded<0):
            errors.append(MetricExceededInferiorLimit(self.rig.name, self.name, self.id, "core temp", self.temp_encoded, 0))
        elif(self.core_temp>self.thresholds.max_core_temp):
            errors.append(MetricExceededSuperiorLimit(self.rig.name, self.name, self.id, "core temp", self.core_temp, self.thresholds.max_core_temp))
        if(self.hr<self.thresholds.min_hr):
            errors.append(MetricExceededInferiorLimit(self.rig.name, self.name, self.id, "hash rate", self.hr, self.thresholds.min_hr))
        if(self.fan_speed<self.thresholds.min_fan_speed):
            errors.append(MetricExceededInferiorLimit(self.rig.name, self.name, self.id, "fan speed", self.fan_speed, self.thresholds.min_fan_speed))
        return errors    


    def __str__(self):
        return "Device(id={}, name={}, status={})".format(self.id, self.name, self.status)

    def __repr__(self):
        return self.__str__()
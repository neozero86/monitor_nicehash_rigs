from Main.problem.bad_core_temp_reading import BadCoreTempReading
from Main.problem.high_core_temp import HighCoreTemp
from Main.problem.high_power import HighPower
from Main.problem.high_vram_temp import HighVRamTemp
from Main.problem.low_fan_speed import LowFanSpeed
from Main.problem.low_hashrate import LowHashRate
from Main.problem.metric_exceeded_inferior_limit import MetricExceededInferiorLimit
from Main.problem.metric_exceeded_superior_limit import MetricExceededSuperiorLimit
from Main.problem.no_vram import NoVram
from Main.problem.unrecognized_device import UnrecognizedDevice
from Main.problem.wrong_status import WrongStatus
from Main.status import Status
from Main.api.api_constants import *

class Device():
    def __init__(self, id, name, rig, status=Status.ACTIVE):
        self.id = id
        self.name = name
        self.rig = rig
        self.status = status
        self.thresholds = None
        self.reset_values()

    def set_threshold(self, device_stats):
        for dev_id, values in device_stats.items():
            if (dev_id in self.name):
                self.thresholds = values
                break

    def update(self, actual_info):
        self.status = actual_info[STATUS]
        if(not self.status.value):
            self.reset_values()
            return False
        self.power = actual_info[POWER]
        self.hr = actual_info[HR]
        self.fan_speed = actual_info[FAN_SPEED]
        if (TEMP_ENCODED in actual_info):
            self.temp_encoded = actual_info[TEMP_ENCODED]
        else:
            self.temp_encoded = 0
        self.core_temp = actual_info[CORE_TEMP]
        #self.hot_spot_temp = actual_info[HOT_SPOT_TEMP]
        self.vram_temp = actual_info[VRAM_TEMP]

    def reset_values(self):
        self.power = 0
        self.hr = 0
        self.fan_speed = 0
        self.temp_encoded = 0
        self.core_temp = 0
        #self.hot_spot_temp = 0
        self.vram_temp = 0

    def check(self):
        errors=[]
        if (not self.thresholds):
            errors.append(UnrecognizedDevice(self.rig.name, 'device [{}] not recognized'.format(self.name)))
            return errors
        if(not self.status.value):
            errors.append(WrongStatus(self.rig.name, self.name, self.id, self.status.name))
            return errors
        if hasattr(self.thresholds, 'max_vram_temp'):
            if(self.vram_temp==-1):
                errors.append(NoVram(self.rig.name, self.name, self.id))
            elif(self.vram_temp>self.thresholds.max_vram_temp):
                errors.append(HighVRamTemp(self.rig.name, self.name, self.id, self.vram_temp, self.thresholds.max_vram_temp))
        if(self.power>self.thresholds.max_power):
            errors.append(HighPower(self.rig.name, self.name, self.id, "power", self.power, self.thresholds.max_power))
        if(self.temp_encoded<0):
            errors.append(BadCoreTempReading(self.rig.name, self.name, self.id))
        elif(self.core_temp>self.thresholds.max_core_temp):
            errors.append(HighCoreTemp(self.rig.name, self.name, self.id, self.core_temp, self.thresholds.max_core_temp))
        if(self.hr<self.thresholds.min_hr):
            errors.append(LowHashRate(self.rig.name, self.name, self.id, "hash rate", self.hr, self.thresholds.min_hr))
        if(self.fan_speed<self.thresholds.min_fan_speed):
            errors.append(LowFanSpeed(self.rig.name, self.name, self.id, "fan speed", self.fan_speed, self.thresholds.min_fan_speed))
        return errors    


    def __str__(self):
        return "Device(id={}, name={}, status={})".format(self.id, self.name, self.status)

    def __repr__(self):
        return self.__str__()
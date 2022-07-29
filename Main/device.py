from Main.status import Status

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
        self.core_temp = 0
        self.hot_spot_temp = 0
        self.vram_temp = 0

    def set_threshold(self, device_stats):
        for dev_id, values in device_stats.items():
            if (dev_id in self.name):
                self.thresholds = values
                break

    def update(self, actual_info, errors):
        self.power = actual_info["powerUsage"]
        self.hr = float(actual_info["speeds"][0]["speed"])
        self.fan_speed = actual_info["revolutionsPerMinutePercentage"]
        self.temp_encoded = actual_info["temperature"]
        self.core_temp = self.temp_encoded % 65536
        self.hot_spot_temp = self.temp_encoded / 65536
        nhqm = actual_info["nhqm"].split(";")
        nhqm = [i for i in nhqm if "=" in i]
        nhqm = {measure.split("=")[0]: measure.split("=")[1] for measure in nhqm}
        if ("MT" not in nhqm):
            errors.append('[{}.{}.{}] no vram metric'.format(self.rig.name, self.name, self.id))
            self.vram_temp = 0
        else:
            self.vram_temp = int(nhqm["MT"])-128	

    def check(self, errors):
        if (not self.thresholds):
            errors.append('Script error [{}.{}] device not recognized'.format(self.rig.name, self.name))
            return False
        if(not self.status.value):
            errors.append('[{}.{}.{}] current status is {}.'.format(self.rig.name, self.name, self.id, self.status.name), errors)
        if(self.vram_temp>self.thresholds.max_vram_temp):
            errors.append('[{}.{}.{}] current vram temp: {} exceed max vram temp {}.'.format(self.rig.name, self.name, self.id, self.vram_temp, self.thresholds.max_vram_temp))
        if(self.power>self.thresholds.max_power):
            errors.append('[{}.{}.{}] current power usage: {} exceed max power {}.'.format(self.rig.name, self.name, self.id, self.power, self.thresholds.max_power))
        if(self.temp_encoded<0):
            errors.append('[{}.{}.{}] negative current core temp: {}.'.format(self.rig.name, self.name, self.id, self.temp_encoded))
        elif(self.core_temp>self.thresholds.max_core_temp):
            errors.append('[{}.{}.{}] current core temp: {} exceed max core temp {}.'.format(self.rig.name, self.name, self.id, self.core_temp, self.thresholds.max_core_temp))
        if(self.hr<self.thresholds.min_hr):
            errors.append('[{}.{}.{}] current hash rate: {} lower than min hash rate {}.'.format(self.rig.name, self.name, self.id, self.hr, self.thresholds.min_hr))
        if(self.fan_speed<self.thresholds.min_fan_speed):
            errors.append('[{}.{}.{}] current fan speed: {} lower than min fan speed {}.'.format(self.rig.name, self.name, self.id, self.fan_speed, self.thresholds.min_fan_speed))


    def __str__(self):
        return "Device(id={}, name={}, status={})".format(self.id, self.name, self.status)

    def __repr__(self):
        return self.__str__()
from Main.device import Device
from Main.status import Status

class Rig():
    def __init__(self, id, name, max_rejected_ratio, algorithm="DAGGERHASHIMOTO"):
        self.id = id
        self.name = name
        self.max_rejected_ratio = max_rejected_ratio
        self.devices = {}
        self.algorithm = algorithm
        self.status = Status.ACTIVE

    def update(self, status):
        status = status["algorithms"]
        if (self.algorithm not in status or not status[self.algorithm]["isActive"]):
            self.status = Status.INACTIVE
            return False
        self.status = Status.ACTIVE
        status = status[self.algorithm]
        self.speed_accepted=status["speedAccepted"]
        self.speed_rejected=status["speedRejected"]
        if (self.speed_accepted != 0): 
            self.rejected_ratio = self.speed_rejected/(self.speed_accepted+self.speed_rejected)
        else:
            self.rejected_ratio = 1

    def update_details(self, actual_info, device_stats):
        self.status = Status[actual_info["minerStatus"]]
        if(not self.status.value):
            return False
        for device_actual_info in actual_info["devices"]:
            id = device_actual_info["id"]
            if (id not in self.devices):
                self.devices[id] = Device(id, device_actual_info["name"], self, Status[device_actual_info["status"]["enumName"]])
            self.devices[id].update(device_actual_info)
        self.set_thresholds(device_stats)
        return True

    def check(self):
        errors = []
        if(not self.status.value):
            errors.append('[{}] host is down.'.format(self.name))
            return errors
        if (self.speed_accepted == 0): 
            errors.append('[{}] speedAccepted = 0.'.format(self.name))
        elif (self.rejected_ratio > self.max_rejected_ratio):
            errors.append('[{}] rejected_ratio = {}%.'.format(self.name,self.rejected_ratio*100))
        for device in self.devices.values():
            errors.extend(device.check())
        return errors

    def set_thresholds(self, device_stats):
        for device in self.devices.values():
            device.set_threshold(device_stats)

    def __str__(self):
        return "Rig(id={}, name={}, devices={}, algorithm={}, status={})".format(self.id, self.name, self.devices, self.algorithm, self.status)
    
    def __repr__(self):
        return self.__str__()
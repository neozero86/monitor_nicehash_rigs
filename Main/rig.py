from Main.device import Device
from Main.problem.device_count_error import DeviceCountError
from Main.problem.high_rejected_ratio import HighRejectedRatio
from Main.problem.host_down import HostDown
from Main.problem.null_accepted_speed import NullAcceptedSpeed
from Main.status import Status
from Main.strategy.down import Down
from Main.strategy.error import Error
from Main.strategy.normal import Normal
import heapq

class Rig():
    def __init__(self, id, name, devices_count, max_rejected_ratio, error_threshold, algorithm="DAGGERHASHIMOTO"):
        self.id = id
        self.name = name
        self.devices_count = devices_count
        self.max_rejected_ratio = max_rejected_ratio
        self.devices = {}
        self.algorithm = algorithm
        self.status = Status.ACTIVE
        self.error_threshold = error_threshold
        self.error_count = 0
        self.total_error_count = 0
        self.problem = None
        self.operation_status = Normal()
        self.solutions = None

    def update(self, status):
        if "algorithms" not in status:
            return False
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
        self.speed = 0
        if "minerStatus" not in actual_info:
            return False
        self.status = Status[actual_info["minerStatus"]]
        if(not self.status.value):
            return False
        if "devices" not in actual_info:
            return False
        for device_actual_info in actual_info["devices"]:
            id = device_actual_info["id"]
            if (id not in self.devices):
                self.devices[id] = Device(id, device_actual_info["name"], self, Status[device_actual_info["status"]["enumName"]])
            self.devices[id].update(device_actual_info)
            self.speed += self.devices[id].hr
        self.set_thresholds(device_stats)
        return True

    def check(self):
        errors = []
        if(not self.status.value):
            errors.append(HostDown(self.name))
        else:
            if (self.speed_accepted == 0): 
                errors.append(NullAcceptedSpeed(self.name))
            elif (self.rejected_ratio > self.max_rejected_ratio):
                errors.append(HighRejectedRatio(self.name,self.rejected_ratio))
            if len(self.devices)!=self.devices_count:
                errors.append(DeviceCountError(self.name, self.devices_count, len(self.devices)))
            for device in self.devices.values():
                errors.extend(device.check())
        if (errors):
            self.error_count += 1
            self.total_error_count += 1
        else:
            self.error_count = 0
            self.problem = None

        if (self.error_count > self.error_threshold and not self.operation_status.should_wait()):
            self.problem = sorted(errors, key=lambda x: x.severity(), reverse=True)[0]
            self.operation_status = Error()
            self.solutions = self.problem.solutions()

        self.operation_status.update()
        return errors

    def solve_errors(self, api, email_sender, logger):
        if (self.problem != None and not self.operation_status.should_wait()):
            solution = self.solutions.pop(0)
            solution.solve(api, self.id, email_sender, self.problem, logger)
            self.operation_status = solution.next_status()
        if(self.problem == None and self.operation_status.is_down()):
            email_sender.send_email(email_content='rig:{} NORMALIZED'.format(self.name))
        if(self.problem == None and not self.operation_status.is_ok()):    
            self.operation_status = Normal()

    def set_thresholds(self, device_stats):
        for device in self.devices.values():
            device.set_threshold(device_stats)

    def __str__(self):
        return "Rig(id={}, name={}, devices={}, algorithm={}, status={})".format(self.id, self.name, self.devices, self.algorithm, self.status)
    
    def __repr__(self):
        return self.__str__()
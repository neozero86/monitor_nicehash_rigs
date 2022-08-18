from Main.device import Device
from Main.problem.device_count_error import DeviceCountError
from Main.problem.high_rejected_ratio import HighRejectedRatio
from Main.problem.host_down import HostDown
from Main.problem.null_accepted_speed import NullAcceptedSpeed
from Main.report.reporter import Reporter
from Main.status import Status
from Main.operational_status.error import Error
from Main.operational_status.normal import Normal
from Main.api.api_constants import *

class Rig():
    def __init__(self, id, name, devices_count, max_rejected_ratio, error_threshold, solution_map, algorithm="DAGGERHASHIMOTO"):
        self.id = id
        self.name = name
        self.devices_count = devices_count
        self.max_rejected_ratio = max_rejected_ratio
        self.solution_map = solution_map
        self.devices = {}
        self.algorithm = algorithm
        self.status = Status.ACTIVE
        self.error_threshold = error_threshold
        self.error_count = 0
        self.total_error_count = 0
        self.problem = None
        self.solution = None
        self.operation_status = Normal()
        self.solutions = None
        self.reset_values()
        self.speed = 0
        self.speed_accepted = 0
        self.speed_rejected = 0
        self.rejected_ratio = 0
        self.unpaid_amount = 0

    def reset_values(self):
        self.speed = 0
        self.speed_accepted = 0
        self.speed_rejected = 0
        self.rejected_ratio = 0
        for device in self.devices.values():
            device.reset_values()

    def update(self, status):
        self.status = status[STATUS]
        if (not self.status.value):
            self.reset_values()
            return False
        self.speed_accepted = status[SPEED_ACCEPTED]
        self.speed_rejected = status[SPEED_REJECTED]
        self.rejected_ratio = status[REJECTED_RATIO]

    def update_details(self, actual_info, device_stats):
        self.speed = 0
        self.status = actual_info[STATUS]
        if(not self.status.value):
            self.reset_values()
            return False
        if (UNPAID_AMOUNT in actual_info):
            if (actual_info[UNPAID_AMOUNT]<self.unpaid_amount):
                Reporter.instance().pay(self.name,self.unpaid_amount)
            self.unpaid_amount = actual_info[UNPAID_AMOUNT]
        if (DAILY_REVENUE in actual_info):
            self.daily_revenue = actual_info[DAILY_REVENUE]
            Reporter.instance().set_daily_revenue(self.name,self.daily_revenue)
        for id, device_actual_info in actual_info[DEVICES].items():
            if (id not in self.devices):
                self.devices[id] = Device(id, device_actual_info[NAME], self)
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
            Reporter.instance().add_interaction_with_error(self.name)
        else:
            self.error_count = 0
            self.problem = None
            self.solutions = None
            self.solution = None

        if (self.error_count > self.error_threshold and not self.operation_status.should_wait()):
            self.problem = sorted(errors, key=lambda x: x.severity(), reverse=True)[0]
            Reporter.instance().add_problem(self.name,self.problem)
            self.operation_status = Error()
            self.solutions = self.getSolutions()

        self.operation_status.update()
        return errors

    def getSolutions(self):
        for problem in self.solution_map.keys():
            if (self.problem.match(problem)):
                return self.solution_map[problem].copy()
        if ("default" in self.solution_map):
            return self.solution_map["default"].copy()
        return self.problem.solutions()

    def solve_errors(self, api, email_sender, logger):
        if (self.problem != None and not self.operation_status.should_wait()):
            self.solution = self.solutions.pop(0)
            Reporter.instance().add_solution(self.name, self.solution)
            self.solution.solve(api, self.id, self.name, email_sender, self.problem, logger)
            self.operation_status = self.solution.next_status()
        if(self.problem == None and self.operation_status.is_down()):
            email_sender.send_email(email_content='rig:{} NORMALIZED'.format(self.name), email_subject='Issue CLOSED Rig {}'.format(self.name))
        if(self.problem == None and not self.operation_status.is_ok()):    
            self.operation_status = Normal()

    def set_thresholds(self, device_stats):
        for device in self.devices.values():
            device.set_threshold(device_stats)

    def __str__(self):
        return "Rig(id={}, name={}, devices={}, algorithm={}, status={})".format(self.id, self.name, self.devices, self.algorithm, self.status)
    
    def __repr__(self):
        return self.__str__()
from Main.api.api_result_constants import *
from Main.status import Status

class ApiAdapter():
    def __init__(self,api, algorithm="DAGGERHASHIMOTO"):
        self.api = api
        self.algorithm = algorithm
    
    def get_my_rig_stats(self, rig_id):
        is_ok = False
        retry = 0
        while (not is_ok and retry < 6):
            try:
                status = self.api.get_my_rig_stats(rig_id)
                is_ok, result = self.parse_status(status)
            except Exception:
                result = {}
                result[STATUS] = Status.INACTIVE
                is_ok = False
            retry += 1
        return result

    def parse_status(self, status):
        result = {}
        result["status"] = Status.INACTIVE
        if "algorithms" not in status:
            return (False, result)
        status = status["algorithms"]
        if (self.algorithm not in status or not status[self.algorithm]["isActive"]):
            return (False, result)
        result[STATUS] = Status.ACTIVE
        status = status[self.algorithm]
        result[SPEED_ACCEPTED] = status["speedAccepted"]
        result[SPEED_REJECTED] = status["speedRejected"]
        if (result[SPEED_ACCEPTED] != 0): 
            result[REJECTED_RATIO] = result["speed_rejected"]/(result["speed_accepted"]+result["speed_rejected"])
        else:
            result[REJECTED_RATIO] = 1
        return (True, result)

    def get_my_rig_details(self, rig_id):
        is_ok = False
        retry = 0
        while (not is_ok and retry < 6):
            try:
                details = self.api.get_my_rig_details(rig_id)
                is_ok, result = self.parse_details(details)
            except Exception:
                result = {}
                result[STATUS] = Status.INACTIVE
                is_ok = False
            retry += 1
        return result

    def parse_details(self, details):
        result = {}
        if "minerStatus" not in details:
            result[STATUS] = Status.INACTIVE
            return (False, result)
        result[STATUS] = Status[details["minerStatus"]]
        if(not result[STATUS].value):
            return (False, result)
        if DEVICES not in details:
            result[STATUS] = Status.INACTIVE
            return (False, result)
        try:
            result[UNPAID_AMOUNT] = float(details["stats"][0]["unpaidAmount"])
        except Exception as e:
            result[STATUS] = Status.INACTIVE
            return (False, result)   
        is_ok = True
        result[DEVICES] = {}
        for device_actual_info in details[DEVICES]:
            device = {}
            device[ID] = device_actual_info["id"]
            device[NAME] = device_actual_info["name"]
            try:
                device[STATUS] = Status[device_actual_info["status"]["enumName"]]
                device[POWER] = device_actual_info["powerUsage"]
                device[HR] = float(device_actual_info["speeds"][0]["speed"])
                device[FAN_SPEED] = device_actual_info["revolutionsPerMinutePercentage"]
                device[TEMP_ENCODED] = device_actual_info["temperature"]
                device[CORE_TEMP] = device[TEMP_ENCODED] % 65536
                device[HOT_SPOT_TEMP] = device[TEMP_ENCODED] / 65536
                nhqm = device_actual_info["nhqm"].split(";")
                nhqm = [i for i in nhqm if "=" in i]
                nhqm = {measure.split("=")[0]: measure.split("=")[1] for measure in nhqm}
                if ("MT" not in nhqm):
                    is_ok = False
                    device[VRAM_TEMP] = -1
                else:
                    device[VRAM_TEMP] = int(nhqm["MT"])-128
            except Exception as e:
                device[STATUS] = Status.INACTIVE
                is_ok = False
            result[DEVICES][device[ID]] = device
        return (is_ok,result)

    def restart_rig(self, rig_id):
        return self.api.restart_rig(rig_id)
    
    def stop_worker(self, rig_id):
        return self.api.stop_worker(rig_id)

    def start_worker(self, rig_id):
        return self.api.start_worker(rig_id)

    def restart_worker(self, rig_id):
        return self.api.restart_worker(rig_id)
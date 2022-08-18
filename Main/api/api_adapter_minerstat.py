from Main.api.api_constants import *
from Main.status import Status

class ApiAdapterMinerstat():
    def __init__(self,api):
        self.api = api
    
    def get_my_rig_stats(self, rig_name):
        is_ok = False
        retry = 0
        while (not is_ok and retry < 6):
            try:
                status = self.api.get_my_rig_details(rig_name)
                is_ok, result = self.parse_status(status)
            except Exception:
                result = {}
                result[STATUS] = Status.INACTIVE
                is_ok = False
            retry += 1
        return result

    def parse_status(self, status):
        result = {}
        if len(status) == 0 or len(status)>1:
            result[STATUS] = Status.INACTIVE
            return (False, result)
        status = list(status.values())[0]
        result[STATUS] = Status.INACTIVE
        if "info" not in status:
            return (False, result)
        if "os" not in status["info"]:
            return (False, result)
        worker_status = Status.from_str(status["info"]["status"])
        os_status = Status.from_str(status["info"]["os"]["status"])
        if (not worker_status.value or not os_status.value):
            return (False, result)
        result[STATUS] = worker_status
        status = status["mining"]
        result[SPEED_ACCEPTED] = status["shares"]["accepted_share"]
        result[SPEED_REJECTED] = status["shares"]["rejected_share"]
        if (result[SPEED_ACCEPTED] != 0): 
            result[REJECTED_RATIO] = result[SPEED_REJECTED]/(result[SPEED_ACCEPTED]+result[SPEED_REJECTED])
        else:
            result[REJECTED_RATIO] = 1
        return (True, result)

    def get_my_rig_details(self, rig_name):
        is_ok = False
        retry = 0
        while (not is_ok and retry < 6):
            try:
                details = self.api.get_my_rig_details(rig_name)
                is_ok, result = self.parse_details(details)
            except Exception:
                result = {}
                result[STATUS] = Status.INACTIVE
                is_ok = False
            retry += 1
        return result

    def parse_details(self, details):
        result = {}
        if len(details) == 0 or len(details)>1:
            result[STATUS] = Status.INACTIVE
            return (False, result)
        details = list(details.values())[0]
        result[STATUS] = Status.from_str(details["info"]["status"])
        if(not result[STATUS].value):
            return (False, result)
        if "hardware" not in details:
            result[STATUS] = Status.INACTIVE
            return (False, result)
        try:
            result[DAILY_REVENUE] = float(details["revenue"]["coin"])
        except Exception as e:
            result[STATUS] = Status.INACTIVE
            return (False, result)   
        is_ok = True
        result[DEVICES] = {}
        i = 0
        for device_actual_info in details["hardware"]:
            device = {}
            device[ID] = i
            device[NAME] = device_actual_info["name"]
            try:
                device[STATUS] = Status.ACTIVE
                device[POWER] = device_actual_info["power"]
                device[HR] = float(device_actual_info["speed"])
                device[FAN_SPEED] = device_actual_info["fan"]
                device[CORE_TEMP] = device_actual_info["temp"]
                if ("memTemp" in device_actual_info):
                    device[VRAM_TEMP] = device_actual_info["memTemp"]
                else:
                    device[VRAM_TEMP] = -1
            except Exception as e:
                device[STATUS] = Status.INACTIVE
                is_ok = False
            result[DEVICES][device[ID]] = device
            i+=1
        return (is_ok,result)

    def restart_rig(self, rig_id):
        return self.api.restart_rig(rig_id)
    
    def stop_worker(self, rig_id):
        return self.api.stop_worker(rig_id)

    def start_worker(self, rig_id):
        return self.api.start_worker(rig_id)

    def restart_worker(self, rig_id):
        return self.api.restart_worker(rig_id)

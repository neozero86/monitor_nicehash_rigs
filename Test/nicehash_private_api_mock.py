import json

class NicehashPrivateApiMock():

    def __init__(self): 
       with open("Test/responses_nicehash.json") as data_file:
            self.responses = json.load(data_file)

    def get_my_rig_stats(self, rig_id):
        return json.loads(self.responses['get_my_rig_stats'][rig_id])

    def get_my_rig_details(self, rig_id):
        return json.loads(self.responses['get_my_rig_details'][rig_id])

    def restart_rig(self, rig_id):
        return {}
    
    def stop_worker(self, rig_id):
        return {}

    def start_worker(self, rig_id):
        return {}

    def restart_worker(self, rig_id):
        return {}
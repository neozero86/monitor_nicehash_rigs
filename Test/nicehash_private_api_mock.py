import json

class NicehashPrivateApiMock():

    def __init__(self): 
       with open("Test/responses.json") as data_file:
            self.responses = json.load(data_file)

    def get_my_rig_stats(self, rig_id):
        return json.loads(self.responses['get_my_rig_stats'][rig_id])

    def get_my_rig_details(self, rig_id):
        return json.loads(self.responses['get_my_rig_details'][rig_id])

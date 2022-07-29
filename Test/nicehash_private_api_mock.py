from pprint import pprint
from Main.nicehash_private_api import NicehashPrivateApi
import json

class NicehashPrivateApiMock(NicehashPrivateApi):

    def __init__(self): 
       super(NicehashPrivateApiMock, self).__init__(None, None, None, None, None)
       with open("Test/responses.json") as data_file:
            self.responses = json.load(data_file)

    def get_my_rig_stats(self, rig_id):
        return json.loads(self.responses['get_my_rig_stats'][rig_id])

    def get_my_rig_details(self, rig_id):
        return json.loads(self.responses['get_my_rig_details'][rig_id])

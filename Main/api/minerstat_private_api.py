import requests, json
from time import sleep

class MinerstatPrivateApi():

    def __init__(self, token, access_key, host='https://api.minerstat.com/v2/'):
        self.token = token
        self.access_key = access_key
        self.host = host

    def get_my_rig_details(self, rig_name):
        return self.__repeated_request('GET', 'stats/' + self.access_key, '/'+rig_name, None, False)

    def restart_rig(self, rig_name):
        return self.__do_action(rig_name, 'reboot')

    def stop_worker(self, rig_name):
        return self.__do_action(rig_name, 'stop')
    
    def start_worker(self, rig_name):
        return self.__do_action(rig_name, 'start')

    def restart_worker(self, rig_name):
        return self.__do_action(rig_name, 'restart')

    def __do_action(self, rig_name, action):
        action_info = {
            "name": rig_name,
            "command": action
        }
        return self.__repeated_request('PATCH', 'worker','', action_info, True)


    def __repeated_request(self, method, path, query, body, use_token):
        result = {}
        count = 0
        while not result and count < 4:
            count += 1
            try:
                result = self.__request(method, path, query, body, use_token)
            except Exception as e:
                result = {}
        return result

    def __request(self, method, path, query, body, use_token):
        url = self.host + path + query
        headers={'Content-Type': 'application/json'}
        if use_token:
            headers['Authorization'] = 'Bearer ' + self.token
        if body:
            body_json = json.dumps(body)
            response = requests.request(method, url, headers=headers, data=body_json)
        else:
            response = requests.request(method, url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)
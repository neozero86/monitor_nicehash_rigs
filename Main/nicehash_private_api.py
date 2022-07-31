from datetime import datetime
from time import mktime, sleep
import uuid
import hmac
import requests
import json
from hashlib import sha256

class NicehashPrivateApi():

    EMPTY_STATUS_REQUEST = "{'algorithms': {}}"
    EMPTY_DETAILS_REQUEST = "'minerStatus': 'OFFLINE'"

    def __init__(self, organisation_id, key, secret, verbose=False, host='https://api2.nicehash.com'):
        self.key = key
        self.secret = secret
        self.organisation_id = organisation_id
        self.host = host
        self.verbose = verbose

    def get_my_rig_stats(self, rig_id):
        return self.__repeated_request('GET', '/main/api/v2/mining/algo/stats', 'rigId=' + rig_id, None)

    def get_my_rig_details(self, rig_id):
        return self.__repeated_request('GET', '/main/api/v2/mining/rig2/'+ rig_id,'', None)

    def restart_rig(self, rig_id):
        return self.__do_action(rig_id, 'RESTART')

    def stop_rig(self, rig_id):
        return self.__do_action(rig_id, 'STOP')
    
    def start_rig(self, rig_id):
        return self.__do_action(rig_id, 'START')

    def restart_worker(self, rig_id):
        self.stop_rig(rig_id)
        sleep(10)
        self.start_rig(rig_id)

    def __do_action(self, rig_id, action):
        action_info = {
            "rigId": rig_id,
            "action": action
        }
        return self.__repeated_request('POST', '/main/api/v2/mining/rigs/status2/','', action_info)

    def __repeated_request(self, method, path, query, body):
        result = {}
        count = 0
        while not result and count < 4:
            count += 1
            try:
                result = self.__request(method, path, query, body)
                if (NicehashPrivateApi.EMPTY_STATUS_REQUEST == str(result) or NicehashPrivateApi.EMPTY_DETAILS_REQUEST in str(result)):
                    result = {}
            except Exception as e:
                result = {}
        return result

    def __request(self, method, path, query, body):

        xtime = self.__get_epoch_ms_from_now()
        xnonce = str(uuid.uuid4())

        message = bytearray(self.key, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(str(xtime), 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(xnonce, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(self.organisation_id, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(method, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(path, 'utf-8')
        message += bytearray('\x00', 'utf-8')
        message += bytearray(query, 'utf-8')

        if body:
            body_json = json.dumps(body)
            message += bytearray('\x00', 'utf-8')
            message += bytearray(body_json, 'utf-8')

        digest = hmac.new(bytearray(self.secret, 'utf-8'), message, sha256).hexdigest()
        xauth = self.key + ":" + digest

        headers = {
            'X-Time': str(xtime),
            'X-Nonce': xnonce,
            'X-Auth': xauth,
            'Content-Type': 'application/json',
            'X-Organization-Id': self.organisation_id,
            'X-Request-Id': str(uuid.uuid4())
        }

        s = requests.Session()
        s.headers = headers

        url = self.host + path
        if query:
            url += '?' + query

        if self.verbose:
            print(method, url)

        if body:
            response = s.request(method, url, data=body_json)
        else:
            response = s.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    def __get_epoch_ms_from_now(self):
        now = datetime.now()
        now_ec_since_epoch = mktime(now.timetuple()) + now.microsecond / 1000000.0
        return int(now_ec_since_epoch * 1000)
import unittest
from Main.monitor import Monitor
from Main.conf import Configuration
from Test.logger_to_variable import LoggerToVariable
from Test.mail_sender_mock import MailSenderMock
from Test.nicehash_private_api_mock import NicehashPrivateApiMock

class MonitorTest(unittest.TestCase):
    
    expected_error_set = set([
        '[id_not_active] host is down.',
        '[id_accepted_speed_0] speedAccepted = 0.',
        '[id_rejected_ratio_high] rejected_ratio = 50.0%.',
        'Script error [id_invalid_profile.Invalid_card] device not recognized',
        '[id_low_hash_rate_id_2.GeForce RTX 3060.2] current hash rate: 25.22 lower than min hash rate 43.0.',
        '[id_low_hash_rate_id_2.GeForce RTX 3060.2] negative current core temp: -1.0.',
        '[id_low_hash_rate_id_2.GeForce RTX 3060.2] no vram metric',
        '[id_power_high.GeForce RTX 3090.0] current power usage: 400.0 exceed max power 350.0.',
        '[id_fan_speed_low.GeForce RTX 3090.0] current fan speed: 4.0 lower than min fan speed 10.0.'
    ])
    
    def setUp(self):
        self.info_list = []
        self.debug_list = []
        self.error_list = []
        conf, rigs, devices = Configuration.constants("Test/conf.json")
        logger = LoggerToVariable(self.info_list, self.debug_list, self.error_list)
        api = NicehashPrivateApiMock()
        email_sender = MailSenderMock()                             
        self.monitor = Monitor(logger, api, email_sender, rigs, devices, conf.error_threshold, conf.max_rejected_ratio, conf.polling_interval_sec, 1)
	

    def test_monitor(self):
        self.monitor.run()
        #print("info_list: {}".format(self.info_list))
        #print("debug_list: {}".format(self.debug_list))
        #print("error_list: {}".format(self.error_list))
        self.assertEqual(self.expected_error_set, set(self.error_list))

if __name__ == '__main__':
    unittest.main()


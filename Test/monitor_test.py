import unittest
from Main.api.api_adapter import ApiAdapter
from Main.monitor import Monitor
from Main.conf import Configuration
from Main.report.reporter import Reporter
from Test.logger_to_variable import LoggerToVariable
from Test.mail_sender_mock import MailSenderMock
from Test.nicehash_private_api_mock import NicehashPrivateApiMock

class MonitorTest(unittest.TestCase):
    
    expected_error_set = set([
        '[name_not_active] host is down',
        '[name_empty] host is down',
        '[name_accepted_speed_0] speedAccepted = 0',
        '[name_rejected_ratio_high] rejected_ratio = 50.0%',
        '[name_invalid_profile.device [Invalid_card] not recognized] device not recognized, check DEVICES variable in conf.json',
        '[name_low_hash_rate_id_2.GeForce RTX 3060.2] current hash rate: 25.22 lower than min hash rate 43.0',
        '[name_low_hash_rate_id_2.GeForce RTX 3060.2] current core temp: -1.0 lower than min core temp 0',
        '[name_low_hash_rate_id_2.GeForce RTX 3060.2] no vram metric',
        '[name_power_high.GeForce RTX 3090.0] current power: 400.0 exceed max power 350.0',
        '[name_fan_speed_low.GeForce RTX 3090.0] current fan speed: 4.0 lower than min fan speed 10.0',
        '[name_power_high] has only 1 devices. The expected amount is 2'
    ])
    emails_sended = ["Daily Report\n================\n\nErrors:\n{   'name_accepted_speed_0': {'NullAcceptedSpeed': 2},\n    'name_empty': {'HostDown': 2},\n    'name_fan_speed_low': {'MetricExceededInferiorLimit': 2},\n    'name_invalid_profile': {'UnrecognizedDevice': 2},\n    'name_low_hash_rate_id_2': {'MetricExceededInferiorLimit': 4, 'NoVram': 2},\n    'name_not_active': {'HostDown': 2},\n    'name_power_high': {   'DeviceCountError': 2,\n                           'MetricExceededSuperiorLimit': 2},\n    'name_rejected_ratio_high': {'HighRejectedRatio': 2}}\n\nProblems:\n{}\n\nSolutions:\n{}\n\nAmount of errors:\n{   'name_accepted_speed_0': 2,\n    'name_empty': 2,\n    'name_fan_speed_low': 2,\n    'name_invalid_profile': 2,\n    'name_low_hash_rate_id_2': 2,\n    'name_not_active': 2,\n    'name_power_high': 2,\n    'name_rejected_ratio_high': 2}\n"]
    
    def setUp(self):
        self.info_list = []
        self.debug_list = []
        self.error_list = []
        conf, rigs, devices = Configuration.constants("Test/conf.json")
        logger = LoggerToVariable(self.info_list, self.debug_list, self.error_list)
        api = NicehashPrivateApiMock()
        api_adapter = ApiAdapter(api)
        self.email_sender = MailSenderMock()            
        Reporter.instance().init(self.email_sender, {"interval_seconds":10, "production": False}, logger)        
        self.monitor = Monitor(logger, api_adapter, self.email_sender, rigs, devices, conf.error_threshold, conf.max_rejected_ratio, conf.polling_interval_sec, 2)

	

    def test_monitor(self):
        self.monitor.run()
        #print("info_list: {}".format(self.info_list))
        #print("debug_list: {}".format(self.debug_list))
        #print("error_list: {}".format(self.error_list))
        Reporter.instance().send_report()
        self.assertEqual(self.expected_error_set, set(self.error_list))
        self.assertEqual(self.emails_sended, self.email_sender.mails_sended)

if __name__ == '__main__':
    unittest.main()


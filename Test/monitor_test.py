import unittest
from Main.api.api_adapter import ApiAdapter
from Main.monitor import Monitor
from Main.conf import Configuration
from Main.report.reporter import Reporter
from Test.logger_to_variable import LoggerToVariable
from Test.mail_sender_mock import MailSenderMock
from Test.nicehash_private_api_mock import NicehashPrivateApiMock
from datetime import datetime

class MonitorTest(unittest.TestCase):
    
    FORMAT = '%d/%m/%y %H:%M:%S'
    
    expected_error_set = set([
        '[name_not_active] host is down',
        '[name_empty] host is down',
        '[name_accepted_speed_0] speedAccepted = 0',
        '[name_rejected_ratio_high] rejected_ratio = 50.0%',
        '[name_invalid_profile.device [Invalid_card] not recognized] device not recognized, check DEVICES variable in conf.json',
        '[name_low_hash_rate_id_2.GeForce RTX 3060.2] current hash rate: 25.22 lower than min hash rate 43.0',
        '[name_low_hash_rate_id_2.GeForce RTX 3060.2] bad core temp reading',
        '[name_low_hash_rate_id_2.GeForce RTX 3060.2] no vram metric',
        '[name_power_high.GeForce RTX 3090.0] current power: 400.0 exceed max power 350.0',
        '[name_fan_speed_low.GeForce RTX 3090.0] current fan speed: 4.0 lower than min fan speed 10.0',
        '[name_power_high] has only 1 devices. The expected amount is 2'
    ])
    def report(frequency):
        return '<p><center><span style="font-size:48px"><u><strong>{} Report</strong></u></span></center></p><p><br />&nbsp;</p><p><span style="color:#cc3300"><span style="font-size:28px"><strong>Profitability</strong></span></span></p><table border=1></table><p><br />&nbsp;</p><p><span style="color:#ff0000"><span style="font-size:28px"><strong>Problems</strong></span></span></p><p><br />&nbsp;</p><p><span style="color:#70ad47"><span style="font-size:28px"><strong>Solutions</strong></span></span></p><p><br />&nbsp;</p><p><span style="color:#cc3300"><span style="font-size:28px"><strong>Accumulated Errors</strong></span></span></p><table border=1><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_empty</strong></span></td><td style="text-align:center; padding: 10px;">2</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_not_active</strong></span></td><td style="text-align:center; padding: 10px;">2</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_accepted_speed_0</strong></span></td><td style="text-align:center; padding: 10px;">2</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_rejected_ratio_high</strong></span></td><td style="text-align:center; padding: 10px;">2</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_invalid_profile</strong></span></td><td style="text-align:center; padding: 10px;">2</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_low_hash_rate_id_2</strong></span></td><td style="text-align:center; padding: 10px;">2</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_power_high</strong></span></td><td style="text-align:center; padding: 10px;">2</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_fan_speed_low</strong></span></td><td style="text-align:center; padding: 10px;">2</td><tr></table><p><br />&nbsp;</p><p><span style="color:#f4b083"><span style="font-size:28px"><strong>Errors Detail</strong></span></span></p><span style="color:#2980b9"><strong><span style="font-size:16px">name_empty</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>2</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_not_active</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>2</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_accepted_speed_0</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NullAcceptedSpeed</td><td>2</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_rejected_ratio_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighRejectedRatio</td><td>2</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_invalid_profile</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>UnrecognizedDevice</td><td>2</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_low_hash_rate_id_2</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NoVram</td><td>2</td></tr><tr><td>BadCoreTempReading</td><td>2</td></tr><tr><td>LowHashRate</td><td>2</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_power_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>DeviceCountError</td><td>2</td></tr><tr><td>HighPower</td><td>2</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_fan_speed_low</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>LowFanSpeed</td><td>2</td></tr></table><br/>'.format(frequency)

    emails_sended_daily = [report('Daily')]
    emails_sended_weely = emails_sended_daily + [report('Weekly')]
    emails_sended_monthly = emails_sended_weely + [report('Monthly')]
    emails_sended_yearly = [report('Daily'), report('Monthly'), report('Yearly')]


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
        self.assertEqual(self.expected_error_set, set(self.error_list))
        Reporter.instance().send_report(datetime.strptime('18/09/19 01:55:19', self.FORMAT))
        self.assertEqual([], self.email_sender.mails_sended)
        Reporter.instance().send_report(datetime.strptime('18/09/19 06:59:19', self.FORMAT))
        self.assertEqual([], self.email_sender.mails_sended)
        Reporter.instance().send_report(datetime.strptime('18/09/19 07:01:19', self.FORMAT))
        self.assertEqual([], self.email_sender.mails_sended)
        Reporter.instance().send_report(datetime.strptime('18/09/19 07:00:19', self.FORMAT))
        self.assertEqual(self.emails_sended_daily, self.email_sender.mails_sended)
        self.email_sender.mails_sended = []
        Reporter.instance().send_report(datetime.strptime('08/08/22 07:00:19', self.FORMAT))
        self.assertEqual(self.emails_sended_weely, self.email_sender.mails_sended)
        self.email_sender.mails_sended = []
        Reporter.instance().send_report(datetime.strptime('01/08/22 07:00:19', self.FORMAT))
        self.assertEqual(self.emails_sended_monthly, self.email_sender.mails_sended)
        self.email_sender.mails_sended = []
        Reporter.instance().send_report(datetime.strptime('01/01/22 07:00:19', self.FORMAT))
        self.assertEqual(self.emails_sended_yearly, self.email_sender.mails_sended)

if __name__ == '__main__':
    unittest.main()


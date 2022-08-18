import unittest
from Main.api.api_adapter_minerstat import ApiAdapterMinerstat
from Main.api.api_adapter_nicehash import ApiAdapterNicehash
from Main.monitor import Monitor
from Main.conf import Configuration
from Main.report.general_status import GeneralStatus
from Main.report.reporter import Reporter
from Test.logger_to_variable import LoggerToVariable
from Test.mail_sender_mock import MailSenderMock
from Test.minerstat_private_api_mock import MinerstatPrivateApiMock
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
        '[name_power_high.GeForce RTX 3090.0] current power: 400.0 exceed max power 350.0',
        '[name_fan_speed_low.GeForce RTX 3090.0] current fan speed: 4.0 lower than min fan speed 10.0',
        '[name_power_high] has only 1 devices. The expected amount is 2',
        '[name_high_core_temp.GeForce RTX 3090.0] current core temp: 80.0 exceed max core temp 68.0',
        'restart worker strategy reached for problem: [name_low_hash_rate_id_2.GeForce RTX 3060.2] current hash rate: 25.22 lower than min hash rate 43.0',
        'restart worker strategy reached for problem: [name_rejected_ratio_high] rejected_ratio = 50.0%',
        'restart worker strategy reached for problem: [name_invalid_profile.device [Invalid_card] not recognized] device not recognized, check DEVICES variable in conf.json',
        'restart worker strategy reached for problem: [name_not_active] host is down',
        'restart worker strategy reached for problem: [name_fan_speed_low.GeForce RTX 3090.0] current fan speed: 4.0 lower than min fan speed 10.0',
        'restart worker strategy reached for problem: [name_power_high] has only 1 devices. The expected amount is 2',
        'stop worker strategy reached for problem: [name_high_core_temp.GeForce RTX 3090.0] current core temp: 80.0 exceed max core temp 68.0',
        'restart worker strategy reached for problem: [name_empty] host is down',
        'restart worker strategy reached for problem: [name_accepted_speed_0] speedAccepted = 0',
        '[name_high_vram_temp.GeForce RTX 3090.0] current VRam temp: 112 exceed max VRam temp 102.0',
        'stop worker strategy reached for problem: [name_high_vram_temp.GeForce RTX 3090.0] current VRam temp: 112 exceed max VRam temp 102.0',
    ])

    expected_error_set_only_nicehash = set([
        '[name_low_hash_rate_id_2.GeForce RTX 3060.2] bad core temp reading',
        '[name_low_hash_rate_id_2.GeForce RTX 3060.2] no vram metric'
    ])

    expected_error_set_only_minerstat = set([
        '[name_no_vram_temp.GeForce RTX 3090.0] no vram metric',
        'restart worker strategy reached for problem: [name_no_vram_temp.GeForce RTX 3090.0] no vram metric'
    ])

    def report_nicehash(frequency):
        return '<p><center><span style="font-size:48px"><u><strong>{} Report</strong></u></span></center></p><p><br />&nbsp;</p><p><span style="color:#cc3300"><span style="font-size:28px"><strong>Profitability</strong></span></span></p><table border=1></table><p><br />&nbsp;</p><p><span style="color:#ff0000"><span style="font-size:28px"><strong>Problems</strong></span></span></p><span style="color:#2980b9"><strong><span style="font-size:16px">name_empty</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_not_active</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_accepted_speed_0</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NullAcceptedSpeed</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_rejected_ratio_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighRejectedRatio</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_invalid_profile</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>UnrecognizedDevice</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_low_hash_rate_id_2</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>LowHashRate</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_power_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>DeviceCountError</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_fan_speed_low</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>LowFanSpeed</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_core_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighCoreTemp</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighVRamTemp</td><td>1</td></tr></table><br/><p><br />&nbsp;</p><p><span style="color:#70ad47"><span style="font-size:28px"><strong>Solutions</strong></span></span></p><span style="color:#2980b9"><strong><span style="font-size:16px">name_empty</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_not_active</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_accepted_speed_0</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_rejected_ratio_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_invalid_profile</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_low_hash_rate_id_2</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_power_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_fan_speed_low</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_core_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>StopWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>StopWorker</td><td>1</td></tr></table><br/><p><br />&nbsp;</p><p><span style="color:#cc3300"><span style="font-size:28px"><strong>Accumulated Errors</strong></span></span></p><table border=1><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_empty</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_not_active</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_accepted_speed_0</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_rejected_ratio_high</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_invalid_profile</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_low_hash_rate_id_2</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_power_high</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_fan_speed_low</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_high_core_temp</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_high_vram_temp</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr></table><p><br />&nbsp;</p><p><span style="color:#f4b083"><span style="font-size:28px"><strong>Errors Detail</strong></span></span></p><span style="color:#2980b9"><strong><span style="font-size:16px">name_empty</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_not_active</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_accepted_speed_0</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NullAcceptedSpeed</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_rejected_ratio_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighRejectedRatio</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_invalid_profile</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>UnrecognizedDevice</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_low_hash_rate_id_2</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NoVram</td><td>5</td></tr><tr><td>BadCoreTempReading</td><td>5</td></tr><tr><td>LowHashRate</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_power_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>DeviceCountError</td><td>5</td></tr><tr><td>HighPower</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_fan_speed_low</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>LowFanSpeed</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_core_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighCoreTemp</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighVRamTemp</td><td>5</td></tr></table><br/>'.format(frequency)

    def report_minerstat(frequency):
        return '<p><center><span style="font-size:48px"><u><strong>{} Report</strong></u></span></center></p><p><br />&nbsp;</p><p><span style="color:#cc3300"><span style="font-size:28px"><strong>Profitability</strong></span></span></p><table border=1></table><p><br />&nbsp;</p><p><span style="color:#ff0000"><span style="font-size:28px"><strong>Problems</strong></span></span></p><span style="color:#2980b9"><strong><span style="font-size:16px">name_empty</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_not_active</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_accepted_speed_0</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NullAcceptedSpeed</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_rejected_ratio_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighRejectedRatio</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_invalid_profile</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>UnrecognizedDevice</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_low_hash_rate_id_2</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>LowHashRate</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_power_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>DeviceCountError</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_fan_speed_low</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>LowFanSpeed</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_core_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighCoreTemp</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_no_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NoVram</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighVRamTemp</td><td>1</td></tr></table><br/><p><br />&nbsp;</p><p><span style="color:#70ad47"><span style="font-size:28px"><strong>Solutions</strong></span></span></p><span style="color:#2980b9"><strong><span style="font-size:16px">name_empty</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_not_active</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_accepted_speed_0</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_rejected_ratio_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_invalid_profile</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_low_hash_rate_id_2</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_power_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_fan_speed_low</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_core_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>StopWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_no_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>RestartWorker</td><td>1</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>StopWorker</td><td>1</td></tr></table><br/><p><br />&nbsp;</p><p><span style="color:#cc3300"><span style="font-size:28px"><strong>Accumulated Errors</strong></span></span></p><table border=1><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_empty</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_not_active</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_accepted_speed_0</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_rejected_ratio_high</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_invalid_profile</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_low_hash_rate_id_2</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_power_high</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_fan_speed_low</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_high_core_temp</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_no_vram_temp</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr><td style="text-align:left; padding: 10px;"><span style="color:#2980b9"><strong>name_high_vram_temp</strong></span></td><td style="text-align:center; padding: 10px;">5</td><tr></table><p><br />&nbsp;</p><p><span style="color:#f4b083"><span style="font-size:28px"><strong>Errors Detail</strong></span></span></p><span style="color:#2980b9"><strong><span style="font-size:16px">name_empty</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_not_active</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HostDown</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_accepted_speed_0</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NullAcceptedSpeed</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_rejected_ratio_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighRejectedRatio</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_invalid_profile</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>UnrecognizedDevice</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_low_hash_rate_id_2</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>LowHashRate</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_power_high</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>DeviceCountError</td><td>5</td></tr><tr><td>HighPower</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_fan_speed_low</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>LowFanSpeed</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_core_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighCoreTemp</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_no_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>NoVram</td><td>5</td></tr></table><br/><span style="color:#2980b9"><strong><span style="font-size:16px">name_high_vram_temp</strong></span></span><table border=0 style="border-spacing: 10px 0rem;"><tr><td>HighVRamTemp</td><td>5</td></tr></table><br/>'.format(frequency)

    def empty_report(frequency):
        return '<p><center><span style="font-size:48px"><u><strong>{} Report</strong></u></span></center></p><p><br />&nbsp;</p><p><span style="color:#cc3300"><span style="font-size:28px"><strong>Profitability</strong></span></span></p><table border=1></table><p><br />&nbsp;</p><p><span style="color:#ff0000"><span style="font-size:28px"><strong>Problems</strong></span></span></p><p><br />&nbsp;</p><p><span style="color:#70ad47"><span style="font-size:28px"><strong>Solutions</strong></span></span></p><p><br />&nbsp;</p><p><span style="color:#cc3300"><span style="font-size:28px"><strong>Accumulated Errors</strong></span></span></p><table border=1></table><p><br />&nbsp;</p><p><span style="color:#f4b083"><span style="font-size:28px"><strong>Errors Detail</strong></span></span></p>'.format(frequency)

    emails_sended_nicehash_daily = [report_nicehash('Daily')]
    emails_sended_nicehash_weely = [empty_report('Daily'), report_nicehash('Weekly')]
    emails_sended_nicehash_monthly = [empty_report('Daily'), empty_report('Weekly'), report_nicehash('Monthly')]
    emails_sended_nicehash_yearly = [empty_report('Daily'), empty_report('Monthly'), report_nicehash('Yearly')]

    emails_sended_minerstat_daily = [report_minerstat('Daily')]
    emails_sended_minerstat_weely = [empty_report('Daily'), report_minerstat('Weekly')]
    emails_sended_minerstat_monthly = [empty_report('Daily'), empty_report('Weekly'), report_minerstat('Monthly')]
    emails_sended_minerstat_yearly = [empty_report('Daily'), empty_report('Monthly'), report_minerstat('Yearly')]


    def setUp(self):
        self.info_list = []
        self.debug_list = []
        self.error_list = []
        self.logger = LoggerToVariable(self.info_list, self.debug_list, self.error_list)
        self.email_sender = MailSenderMock()            
        Reporter.instance().init(self.email_sender, {"interval_seconds":10, "production": False}, self.logger)  
        GeneralStatus.instance().init("test")      	

    def test_monitor_nicehash(self):
        self.load_nicehash_settings()

        self.monitor.run()
        #print("info_list: {}".format(self.info_list))
        #print("debug_list: {}".format(self.debug_list))
        #print("error_list: {}".format(self.error_list))
        self.assertEqual(self.expected_error_set.union(self.expected_error_set_only_nicehash), set(self.error_list))
        self.check_emails_sended(self.emails_sended_nicehash_daily, self.emails_sended_nicehash_weely, self.emails_sended_nicehash_monthly, self.emails_sended_nicehash_yearly)

    def check_emails_sended(self, expected_mails_daily, expected_mails_weekly, expected_mails_monthly, expected_mails_yearly):
        Reporter.instance().send_report(datetime.strptime('18/09/19 01:55:19', self.FORMAT))
        self.assertEqual([], self.email_sender.mails_sended)
        Reporter.instance().send_report(datetime.strptime('18/09/19 03:59:19', self.FORMAT))
        self.assertEqual([], self.email_sender.mails_sended)
        Reporter.instance().send_report(datetime.strptime('18/09/19 04:01:19', self.FORMAT))
        self.assertEqual([], self.email_sender.mails_sended)
        Reporter.instance().send_report(datetime.strptime('18/09/19 04:00:19', self.FORMAT))
        #self.assertEqual(len(expected_mails_daily), len(self.email_sender.mails_sended))
        self.assertEqual(expected_mails_daily, self.email_sender.mails_sended)
        self.email_sender.mails_sended = []
        Reporter.instance().send_report(datetime.strptime('08/08/22 04:00:19', self.FORMAT))
        self.assertEqual(len(expected_mails_weekly), len(self.email_sender.mails_sended))
        self.assertEqual(expected_mails_weekly, self.email_sender.mails_sended)
        self.email_sender.mails_sended = []
        Reporter.instance().send_report(datetime.strptime('01/08/22 04:00:19', self.FORMAT))
        self.assertEqual(len(expected_mails_monthly), len(self.email_sender.mails_sended))
        self.assertEqual(expected_mails_monthly, self.email_sender.mails_sended)
        self.email_sender.mails_sended = []
        Reporter.instance().send_report(datetime.strptime('01/01/22 04:00:19', self.FORMAT))
        self.assertEqual(len(expected_mails_yearly), len(self.email_sender.mails_sended))
        self.assertEqual(expected_mails_yearly, self.email_sender.mails_sended)

    def test_monitor_minerstat(self):
        self.load_minerstat_settings()

        self.monitor.run()
        #print("info_list: {}".format(self.info_list))
        #print("debug_list: {}".format(self.debug_list))
        #print("error_list: {}".format(self.error_list))
        self.assertEqual(self.expected_error_set.union(self.expected_error_set_only_minerstat), set(self.error_list))
        self.check_emails_sended(self.emails_sended_minerstat_daily, self.emails_sended_minerstat_weely, self.emails_sended_minerstat_monthly, self.emails_sended_minerstat_yearly)

    def load_nicehash_settings(self):
        conf, rigs, devices, solution_map = Configuration.constants("Test/nicehash_conf.json")
        api = NicehashPrivateApiMock()
        api_adapter = ApiAdapterNicehash(api)
        self.monitor = Monitor(self.logger, api_adapter, self.email_sender, rigs, devices, conf.error_threshold, conf.max_rejected_ratio, solution_map, conf.polling_interval_sec, 5)


    def load_minerstat_settings(self):
        conf, rigs, devices, solution_map = Configuration.constants("Test/minerstat_conf.json")
        api = MinerstatPrivateApiMock()
        api_adapter = ApiAdapterMinerstat(api)
        self.monitor = Monitor(self.logger, api_adapter, self.email_sender, rigs, devices, conf.error_threshold, conf.max_rejected_ratio, solution_map, conf.polling_interval_sec, 5)


if __name__ == '__main__':
    unittest.main()


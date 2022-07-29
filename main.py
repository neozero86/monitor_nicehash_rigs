import nicehash
import json
from conf import logger, c
from mail_sender import AlertEmailSender
from pprint import pprint
from time import sleep, time

EMAIL_SENDER = AlertEmailSender(c.mail.gmail_username,
                                    c.mail.gmail_password,
                                    c.mail.notification_email,
                                    c.mail.email_subject)

PRIVATE_API = nicehash.private_api(c.organisation_id, c.key, c.secret)
RIGS = {k[2:]: v for k ,v in c.rigs._asdict().items()}
DEVICES = {k[2:].replace("_"," "): v for k ,v in c.devices._asdict().items()}

def monitor():
	print(DEVICES)
	while True:
		try:
			for rig_name,rig_id in RIGS.items():
				logger.info(rig_name)
				if (check_status(rig_name, rig_id)):
					check_details(rig_name, rig_id)
		except Exception as e:
			logger.error(e)
			EMAIL_SENDER.send_email(email_content='Script error [{}]'.format(str(e)))
		logger.debug('Going to sleep for {} seconds.'.format(c.polling_interval_sec))
		sleep(c.polling_interval_sec)

def check_status(rig_name, rig_id):
	status = PRIVATE_API.get_my_rig_stats(rig_id)
	logger.info(status)
	status = status["algorithms"]["DAGGERHASHIMOTO"]
	if (not status["isActive"]):
		EMAIL_SENDER.send_email(email_content='[{}] host is disabled. Please check.'.format(
                            rig_name))
		logger.error('[{}] host is disabled'.format(rig_name))
		return False
	accepted=status["speedAccepted"]
	rejected=status["speedRejected"]
	if (accepted==0):
		EMAIL_SENDER.send_email(email_content='[{}] speedAccepted = 0. Please check.'.format(
                            rig_name))
	rejected_ratio = rejected/(accepted+rejected)
	if (rejected_ratio>c.max_rejected_ratio):
		EMAIL_SENDER.send_email(email_content='[{}] rejected_ratio = {}%. Please check.'.format(
                            rig_name,rejected_ratio*100))
	return True

def check_details(rig_name, rig_id):
	details = PRIVATE_API.get_my_rig_details(rig_id)
	logger.debug(details)
	status = details["minerStatus"]
	if (status != "MINING"):
		EMAIL_SENDER.send_email(email_content='[{}] host is down. Please check.'.format(
                    rig_name))
	for device in details["devices"]:
		name = device["name"]
		found = False
		for dev_id, values in DEVICES.items():
			if (dev_id in name):
				logger.debug('profile: {} for {}'.format(dev_id, name))
				check(rig_name, device, values.max_power, values.max_tem, values.min_hr, values.min_fan_speed)
				found = True
				break
		if (not found):
			logger.error('Script error [{}.{}] device not recognized'.format(rig_name, name))
			EMAIL_SENDER.send_email(email_content='Script error [{}.{}] device not recognized'.format(rig_name, name))


def check(rig_name, device, max_power, max_tem, min_hr, min_fan_speed):
	name= device["name"]
	power = device["powerUsage"]
	temp = device["temperature"]%65536
	hr = float(device["speeds"][0]["speed"])
	fan_speed = device["revolutionsPerMinutePercentage"]
	status = device["status"]["enumName"]
	if(status != "MINING"):
		EMAIL_SENDER.send_email(email_content='[{}.{}] current status is {}. Please check.'.format(
		                            rig_name, name, status))
	if(power>max_power):
		EMAIL_SENDER.send_email(email_content='[{}.{}] current power usage: {} exceed max power {}. Please check.'.format(
		                            rig_name, name, power, max_power))
	if(temp>max_tem):
		EMAIL_SENDER.send_email(email_content='[{}.{}] current temp: {} exceed max temp {}. Please check.'.format(
	                            rig_name, name, temp, max_tem))
	if(hr<min_hr):
		EMAIL_SENDER.send_email(email_content='[{}.{}] current hash rate: {} lower than min hash rate {}. Please check.'.format(
	                            rig_name, name, hr, min_hr))
	if(fan_speed<min_fan_speed):
		EMAIL_SENDER.send_email(email_content='[{}.{}] current fan speed: {} lower than min fan speed {}. Please check.'.format(
	                            rig_name, name, fan_speed, min_fan_speed))

if __name__ == '__main__':
    monitor()

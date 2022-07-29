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
	error_count = 0
	while True:
		errors = []
		for rig_name,rig_id in RIGS.items():
			try:
				logger.info(rig_name)
				if (check_status(rig_name, rig_id, errors)):
					check_details(rig_name, rig_id, errors)
			except Exception as e:
				error('Rig: {}; Script error [{}]'.format(rig_name, str(e)), errors, True)
		if (errors):
			error_count += 1
		else:
			error_count = 0

		logger.info('accumulated errors: {}'.format(error_count))
		logger.info('Going to sleep for {} seconds.'.format(c.polling_interval_sec))
		send_email_threshold_reached(errors, c.error_threshold, error_count)
		sleep(c.polling_interval_sec)

def check_status(rig_name, rig_id, errors):
	status = PRIVATE_API.get_my_rig_stats(rig_id)
	logger.info(status)
	status = status["algorithms"]["DAGGERHASHIMOTO"]
	if (not status["isActive"]):
		error('[{}] host is disabled.'.format(rig_name), errors)
		return False
	accepted=status["speedAccepted"]
	rejected=status["speedRejected"]
	if (accepted==0):
		error('[{}] speedAccepted = 0.'.format(rig_name), errors)
	else:	
		rejected_ratio = rejected/(accepted+rejected)
		if (rejected_ratio>c.max_rejected_ratio):
			error('[{}] rejected_ratio = {}%.'.format(rig_name,rejected_ratio*100), errors)
	return True

def check_details(rig_name, rig_id, errors):
	details = PRIVATE_API.get_my_rig_details(rig_id)
	logger.debug(details)
	status = details["minerStatus"]
	if (status != "MINING"):
		error('[{}] host is down.'.format(rig_name), errors)
		return False
	for device in details["devices"]:
		name = device["name"]
		found = False
		for dev_id, values in DEVICES.items():
			if (dev_id in name):
				logger.debug('profile: {} for {}'.format(dev_id, name))
				check(rig_name, device, values.max_power, values.max_tem, values.min_hr, values.min_fan_speed, errors)
				found = True
				break
		if (not found):
			error('Script error [{}.{}] device not recognized'.format(rig_name, name), errors, True)
	return True

def check(rig_name, device, max_power, max_tem, min_hr, min_fan_speed, errors):
	name= device["name"]
	power = device["powerUsage"]
	temp = device["temperature"]%65536
	hr = float(device["speeds"][0]["speed"])
	fan_speed = device["revolutionsPerMinutePercentage"]
	status = device["status"]["enumName"]
	if(status != "MINING"):
		error('[{}.{}] current status is {}.'.format(rig_name, name, status), errors)
		return False
	if(power>max_power):
		error('[{}.{}] current power usage: {} exceed max power {}.'.format(rig_name, name, power, max_power), errors)
	if(temp>max_tem):
		error('[{}.{}] current temp: {} exceed max temp {}.'.format(rig_name, name, temp, max_tem), errors)
	if(hr<min_hr):
		error('[{}.{}] current hash rate: {} lower than min hash rate {}.'.format(rig_name, name, hr, min_hr), errors)
	if(fan_speed<min_fan_speed):
		error('[{}.{}] current fan speed: {} lower than min fan speed {}.'.format(rig_name, name, fan_speed, min_fan_speed), errors)

def error(message, errors, send_email=False):
	logger.error(message)
	errors.append(message)
	if (send_email):
		EMAIL_SENDER.send_email(email_content=message)

def send_email_threshold_reached(errors, error_threshold, error_count):
	if (error_count>=error_threshold):
		logger.error('error_count: {}, sending email'.format(error_count))
		EMAIL_SENDER.send_email(email_content='\n'.join(errors))
if __name__ == '__main__':
    monitor()

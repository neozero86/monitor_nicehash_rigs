from time import sleep

class Monitor():
	def __init__(self, logger, api, email_sender, rigs, devices, error_threshold, max_rejected_ratio, polling_interval_sec, iterations = -1):
		self.logger = logger
		self.api = api
		self.email_sender = email_sender
		self.rigs = rigs
		self.devices = devices
		self.error_threshold = error_threshold
		self.max_rejected_ratio = max_rejected_ratio
		self.polling_interval_sec = polling_interval_sec
		self.iterations = iterations

	def run(self):
		error_count = 0
		while True:
			errors = []
			for rig_name,rig_id in self.rigs.items():
				try:
					self.logger.info(rig_name)
					if (self.check_status(rig_name, rig_id, errors)):
						self.check_details(rig_name, rig_id, errors)
				except Exception as e:
					self.error('Rig: {}; Script error [{}]'.format(rig_name, str(e)), errors, True)
			if (errors):
				error_count += 1
			else:
				error_count = 0

			self.logger.info('accumulated errors: {}'.format(error_count))
			self.logger.info('Going to sleep for {} seconds.'.format(self.polling_interval_sec))
			self.send_email_threshold_reached(errors, self.error_threshold, error_count)
			
			if (self.iterations != -1):
				self.iterations -= 1
				if (self.iterations == 0):
					break
				
			sleep(self.polling_interval_sec)

	def check_status(self, rig_name, rig_id, errors):
		status = self.api.get_my_rig_stats(rig_id)
		self.logger.info(status)
		status = status["algorithms"]
		if ("DAGGERHASHIMOTO" not in status or not status["DAGGERHASHIMOTO"]["isActive"]):
			self.error('[{}] host is down.'.format(rig_name), errors)
			return False
		status = status["DAGGERHASHIMOTO"]

		accepted=status["speedAccepted"]
		rejected=status["speedRejected"]
		if (accepted==0):
			self.error('[{}] speedAccepted = 0.'.format(rig_name), errors)
		else:	
			rejected_ratio = rejected/(accepted+rejected)
			if (rejected_ratio > self.max_rejected_ratio):
				self.error('[{}] rejected_ratio = {}%.'.format(rig_name,rejected_ratio*100), errors)
		return True

	def check_details(self, rig_name, rig_id, errors):
		details = self.api.get_my_rig_details(rig_id)
		self.logger.debug(details)
		status = details["minerStatus"]
		if (status != "MINING"):
			self.error('[{}] host is down.'.format(rig_name), errors)
			return False
		for device in details["devices"]:
			name = device["name"]
			found = False
			for dev_id, values in self.devices.items():
				if (dev_id in name):
					self.logger.debug('profile: {} for {}'.format(dev_id, name))
					self.check(rig_name, device, values.max_power, values.max_core_temp, values.max_vram_temp, values.min_hr, values.min_fan_speed, errors)
					found = True
					break
			if (not found):
				self.error('Script error [{}.{}] device not recognized'.format(rig_name, name), errors, True)
		return True

	def check(self, rig_name, device, max_power, max_core_temp, max_vram_temp, min_hr, min_fan_speed, errors):
		name= device["name"]
		device_id= device["id"]
		status = device["status"]["enumName"]
		if(status != "MINING"):
			self.error('[{}.{}.{}] current status is {}.'.format(rig_name, name, device_id, status), errors)
			return False
		power = device["powerUsage"]
		hr = float(device["speeds"][0]["speed"])
		fan_speed = device["revolutionsPerMinutePercentage"]
		temp_encoded = device["temperature"]
		core_temp = temp_encoded % 65536
		hot_spot_temp = temp_encoded / 65536
		nhqm = device["nhqm"].split(";")
		nhqm = [i for i in nhqm if "=" in i]
		nhqm = {measure.split("=")[0]: measure.split("=")[1] for measure in nhqm}
		if ("MT" not in nhqm):
			self.error('[{}.{}.{}] no vram metric'.format(rig_name, name, device_id), errors)
		else:
			vram_temp = int(nhqm["MT"])-128	
			if(vram_temp>max_vram_temp):
				self.error('[{}.{}.{}] current vram temp: {} exceed max vram temp {}.'.format(rig_name, name, device_id, vram_temp, max_vram_temp), errors)
		if(power>max_power):
			self.error('[{}.{}.{}] current power usage: {} exceed max power {}.'.format(rig_name, name, device_id, power, max_power), errors)
		if(temp_encoded<0):
			self.error('[{}.{}.{}] negative current core temp: {}.'.format(rig_name, name, device_id, temp_encoded), errors)
		elif(core_temp>max_core_temp):
			self.error('[{}.{}.{}] current core temp: {} exceed max core temp {}.'.format(rig_name, name, device_id, core_temp, max_core_temp), errors)
		if(hr<min_hr):
			self.error('[{}.{}.{}] current hash rate: {} lower than min hash rate {}.'.format(rig_name, name, device_id, hr, min_hr), errors)
		if(fan_speed<min_fan_speed):
			self.error('[{}.{}.{}] current fan speed: {} lower than min fan speed {}.'.format(rig_name, name, device_id, fan_speed, min_fan_speed), errors)

	def error(self, message, errors, send_email=False):
		self.logger.error(message)
		errors.append(message)
		if (send_email):
			self.email_sender.send_email(email_content=message)

	def send_email_threshold_reached(self, errors, error_threshold, error_count):
		if (error_count>=error_threshold):
			self.logger.error('error_count: {}, sending email'.format(error_count))
			self.email_sender.send_email(email_content='\n'.join(errors))
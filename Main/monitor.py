from time import sleep

from requests import RequestException
from Main.problem.script_error import ScriptError
from Main.report.reporter import Reporter

from Main.rig import Rig

class Monitor():
    def __init__(self, logger, api, email_sender, rigs, devices, error_threshold, max_rejected_ratio, polling_interval_sec, iterations = -1):
        self.logger = logger
        self.api = api
        self.email_sender = email_sender
        self.rigs = [Rig(v.id,k,v.devices, max_rejected_ratio, error_threshold) for k,v in rigs.items()]
        self.devices = devices
        self.error_threshold = error_threshold
        self.polling_interval_sec = polling_interval_sec
        self.iterations = iterations

    def run(self):
        while True:
            errors = []
            for rig in self.rigs:
                try:
                    if (self.update_status(rig)):
                        self.update_details(rig)
                    self.logInfo(rig)                    
                    rig_errors = rig.check()
                    Reporter.instance().add_errors(rig.name, rig_errors)
                    errors.extend(rig_errors)
                    rig.solve_errors(self.api, self.email_sender, self.logger)
                except Exception as e:
                    error = ScriptError(rig.name, e)
                    errors.append(error)
                    self.email_sender.send_email(email_content=str(error))

            self.logger.debug('')
            self.logger.debug('')
            self.logger.debug('')
            for error in errors:
                self.logger.error(str(error))
            self.logger.info('Going to sleep for {} seconds.'.format(self.polling_interval_sec))

            if (self.iterations != -1):
                self.iterations -= 1
                if (self.iterations == 0):
                    break
                
            sleep(self.polling_interval_sec)

    def logInfo(self, rig):
        self.logger.info(rig.name)
        self.logger.info('Status: {}'.format(rig.status))
        self.logger.info('Operation Status: {}'.format(rig.operation_status))
        self.logger.info('Speed: {}'.format(rig.speed))
        self.logger.info('Problem: {}'.format(rig.problem))
        self.logger.info('Solutions: {}'.format(rig.solutions))
        self.logger.debug('Rejected: {}'.format(rig.speed_rejected))
        self.logger.debug('Accepted: {}'.format(rig.speed_accepted/1000000))
        self.logger.info('Rejected ratio: {}'.format(rig.rejected_ratio))
        self.logger.debug('Devices:')
        for device in rig.devices.values():
            self.logger.debug('  Device name: {}'.format(device.name))
            self.logger.debug('  Device name: {}'.format(device.id))
            self.logger.debug('  Device status: {}'.format(device.status))
            self.logger.debug('  Device Hash rate: {}'.format(device.hr))
            self.logger.debug('  Device Core Temp: {}'.format(device.core_temp))
            self.logger.debug('  Device VRam Temp: {}'.format(device.vram_temp))
            self.logger.debug('  Device Fan speed: {}'.format(device.fan_speed))
            self.logger.debug('  Device Power: {}'.format(device.power))
            self.logger.debug('  Device Hot Spot Temp: {}'.format(device.hot_spot_temp))
        self.logger.info('')
        self.logger.debug('')


    def update_status(self, rig):
        status = self.api.get_my_rig_stats(rig.id)
        self.logger.debug(status)
        rig.update(status)
        return rig.status.value        

    def update_details(self, rig):
        details = self.api.get_my_rig_details(rig.id)
        self.logger.debug(details)
        rig.update_details(details, self.devices)
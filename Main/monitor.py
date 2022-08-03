from time import sleep

from requests import RequestException
from Main.problem.script_error import ScriptError

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
                    self.logger.info(rig.name)
                    if (self.update_status(rig)):
                        self.update_details(rig)
                    errors.extend(rig.check())
                    rig.solve_errors(self.api, self.email_sender, self.logger)
                except RequestException:
                    error = ScriptError(rig.name, e)
                    errors.append(error)
                except Exception as e:
                    error = ScriptError(rig.name, e)
                    errors.append(error)
                    self.email_sender.send_email(email_content=str(error))

            for error in errors:
                self.logger.error(str(error))
            self.logger.info('Going to sleep for {} seconds.'.format(self.polling_interval_sec))

            if (self.iterations != -1):
                self.iterations -= 1
                if (self.iterations == 0):
                    break
                
            sleep(self.polling_interval_sec)

    def update_status(self, rig):
        status = self.api.get_my_rig_stats(rig.id)
        self.logger.info(status)
        rig.update(status)
        return rig.status.value        

    def update_details(self, rig):
        details = self.api.get_my_rig_details(rig.id)
        self.logger.debug(details)
        rig.update_details(details, self.devices)
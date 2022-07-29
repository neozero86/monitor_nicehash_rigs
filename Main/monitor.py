from time import sleep
from Main.problem.script_error import ScriptError

from Main.rig import Rig

class Monitor():
    def __init__(self, logger, api, email_sender, rigs, devices, error_threshold, max_rejected_ratio, polling_interval_sec, iterations = -1):
        self.logger = logger
        self.api = api
        self.email_sender = email_sender
        self.rigs = [Rig(v,k, max_rejected_ratio, error_threshold) for k,v in rigs.items()]
        self.devices = devices
        self.error_threshold = error_threshold
        self.polling_interval_sec = polling_interval_sec
        self.iterations = iterations

    def run(self):
        error_count = 0
        while True:
            errors = []
            for rig in self.rigs:
                try:
                    self.logger.info(rig.name)
                    if (self.update_status(rig)):
                        self.update_details(rig)
                    errors.extend(rig.check())
                except Exception as e:
                    errors.append(ScriptError(rig.name, e))
            if (errors):
                error_count += 1
            else:
                error_count = 0
            for error in errors:
                self.logger.error(str(error))
            self.logger.info('accumulated errors: {}'.format(error_count))
            self.logger.info('Going to sleep for {} seconds.'.format(self.polling_interval_sec))
            self.send_email_threshold_reached(errors, self.error_threshold, error_count)
            
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
     
    def send_email_threshold_reached(self, errors, error_threshold, error_count):
        if (error_count>=error_threshold):
            self.logger.error('error_count: {}, sending email'.format(error_count))
            self.email_sender.send_email(email_content='\n'.join([str(e) for e in errors]))
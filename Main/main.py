from Main.api.api_adapter_minerstat import ApiAdapterMinerstat
from Main.api.api_adapter_nicehash import ApiAdapterNicehash
from Main.api.minerstat_private_api import MinerstatPrivateApi
from Main.api.nicehash_private_api import NicehashPrivateApi
from Main.monitor import Monitor
from Main.conf import Configuration
from Main.logger import Logger
from Main.mail_sender import MailSender
from Main.report.reporter import Reporter
from Main.api.api_constants import *

def main():
    conf, rigs, devices, solution_map = Configuration.constants()
    logger = Logger()
    if (conf.api == NICEHASH):
        api = NicehashPrivateApi(conf.organisation_id, conf.key, conf.secret)
        api_adapter = ApiAdapterNicehash(api)
    elif (conf.api == MINERSTAT):
        api = MinerstatPrivateApi(conf.api_token, conf.access_key)
        api_adapter = ApiAdapterMinerstat(api)
    else:
        raise Exception("Invalid API")
    email_sender = MailSender(conf.mail.gmail_username,
                                    conf.mail.gmail_password,
                                    conf.mail.notification_email,
                                    conf.mail.email_subject)
    Reporter.instance().init(email_sender, {"interval_seconds":60, "production": True}, logger)
    monitor = Monitor(logger, api_adapter, email_sender, rigs, devices,
    conf.error_threshold, conf.max_rejected_ratio, solution_map, conf.polling_interval_sec)
    monitor.run()
if __name__ == '__main__':
    main()

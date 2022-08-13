from Main.api.api_adapter import ApiAdapter
from Main.api.nicehash_private_api import NicehashPrivateApi
from Main.monitor import Monitor
from Main.conf import Configuration
from Main.logger import Logger
from Main.mail_sender import MailSender
from Main.report.reporter import Reporter

def main():
    conf, rigs, devices = Configuration.constants()
    logger = Logger()
    api = NicehashPrivateApi(conf.organisation_id, conf.key, conf.secret)
    api_adapter = ApiAdapter(api)
    email_sender = MailSender(conf.mail.gmail_username,
                                    conf.mail.gmail_password,
                                    conf.mail.notification_email,
                                    conf.mail.email_subject)
    Reporter.instance().init(email_sender, {"interval_seconds":30, "production": True}, logger)
    monitor = Monitor(logger, api_adapter, email_sender, rigs, devices,
    conf.error_threshold, conf.max_rejected_ratio, conf.polling_interval_sec)
    monitor.run()
if __name__ == '__main__':
    main()

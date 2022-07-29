from Main.nicehash_private_api import NicehashPrivateApi
from Main.monitor import Monitor
from Main.conf import Configuration
from Main.logger import Logger
from Main.mail_sender import MailSender

def main():
	conf, rigs, devices = Configuration.constants()
	logger = Logger()
	api = NicehashPrivateApi(conf.organisation_id, conf.key, conf.secret)
	email_sender = MailSender(conf.mail.gmail_username,
                                    conf.mail.gmail_password,
                                    conf.mail.notification_email,
                                    conf.mail.email_subject)
			
	monitor = Monitor(logger, api, email_sender, rigs, devices, conf.error_threshold, conf.max_rejected_ratio, conf.polling_interval_sec)
	monitor.run()
if __name__ == '__main__':
    main()

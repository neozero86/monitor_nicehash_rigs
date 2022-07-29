import nicehash
from Main.monitor import Monitor
from Main.conf import c
from Main.logger import Logger
from Main.mail_sender import AlertEmailSender

EMAIL_SENDER = AlertEmailSender(c.mail.gmail_username,
                                    c.mail.gmail_password,
                                    c.mail.notification_email,
                                    c.mail.email_subject)

PRIVATE_API = nicehash.private_api(c.organisation_id, c.key, c.secret)
RIGS = {k[2:]: v for k ,v in c.rigs._asdict().items()}
DEVICES = {k[2:].replace("_"," "): v for k ,v in c.devices._asdict().items()}


def main():
	logger = Logger()
	api = nicehash.private_api(c.organisation_id, c.key, c.secret)
	email_sender = AlertEmailSender(c.mail.gmail_username,
                                    c.mail.gmail_password,
                                    c.mail.notification_email,
                                    c.mail.email_subject)
									
	monitor = Monitor(logger, api, email_sender, c.polling_interval_sec)
	monitor.run()
if __name__ == '__main__':
    main()

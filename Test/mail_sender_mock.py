from Main.mail_sender import MailSender


class MailSenderMock(MailSender):
    def __init__(self):
       super(MailSenderMock, self).__init__(None, None, None, None)

    def send_email(self, email_content):
        pass

    def send_email_notification(self, gmail_user, gmail_password, target_email, email_content, email_subject):
        pass

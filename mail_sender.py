from conf import logger
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = "smtp.gmail.com" # for Gmail
port = 587  # For starttls

class AlertEmailSender:
    def __init__(self, gmail_user, gmail_password, target_email, email_subject):
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
        self.target_email = target_email
        self.email_subject = email_subject

    def send_email(self, email_content):
        send_email_notification(self.gmail_user,
                                self.gmail_password,
                                self.target_email,
                                email_content,
                                self.email_subject)
        logger.debug('Email sent for subject = {}, content = {}'.format(self.email_subject, email_content))

def send_email_notification(gmail_user, gmail_password, target_email, email_content, email_subject):
    user = '{}@gmail.com'.format(gmail_user)
    context = ssl.create_default_context()

    msg = MIMEMultipart()
    msg["Subject"] = email_subject
    msg["From"] = user
    msg['To'] = ", ".join(target_email)
    msg.attach(MIMEText(email_content, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # check connection
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # check connection
        server.login(user, gmail_password)

        # Send email here
        server.sendmail(user, target_email, msg.as_string())

    except Exception as e:
        # Print any error messages 
        print(e)
    finally:
        server.quit()

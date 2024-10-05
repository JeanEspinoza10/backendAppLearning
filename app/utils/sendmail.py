from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()

class SendMail:
    def __init__(self):
        self.client = smtplib.SMTP_SSL("smtp.gmail.com")
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.client.login(self.user, self.password )
        self.objectEmail = EmailMessage()

    def send(self, to, subject, message):
        try:
            self.objectEmail["From"] = self.user
            self.objectEmail["To"] = to
            self.objectEmail["Subject"] = subject
            self.objectEmail.set_content(message)
            self.client.sendmail(self.user, to, self.objectEmail.as_string())
            self.client.quit()
            return True
        except Exception as e:
            return False

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from secret_config import (MAIL_FROM_ADDRESS, MAIL_SERVER,
                           MAIL_FROM_PASSWORD, MAIL_TO_ADDRESS)


def send_email(body, subject):
    msg = MIMEMultipart()
    msg['From'] = MAIL_FROM_ADDRESS
    msg['To'] = MAIL_TO_ADDRESS
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    message = msg.as_string()

    try:
        server = smtplib.SMTP(MAIL_SERVER)
        server.starttls()
        server.login(MAIL_FROM_ADDRESS, MAIL_FROM_PASSWORD)

        server.sendmail(MAIL_FROM_ADDRESS, MAIL_TO_ADDRESS, message)
        server.quit()

    except Exception as e:
        print("FAILURE - Email not sent")
        print(e)

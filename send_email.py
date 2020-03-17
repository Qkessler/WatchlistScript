# I import my secret config. I have created a config file for other users,
# just update the info there and uncomment the next line.
# import config
import secret_config as config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(body, subject):
    msg = MIMEMultipart()
    msg['From'] = config.mailFromAddress
    msg['To'] = config.mailToAddress
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    message = msg.as_string()

    try:
        server = smtplib.SMTP(config.mailServer)
        server.starttls()
        server.login(config.mailFromAddress, config.mailFromPassword)

        server.sendmail(config.mailFromAddress, config.mailToAddress, message)
        server.quit()
        # print("SUCCESS - Email sent")

    except Exception as e:
        print("FAILURE - Email not sent")
        print(e)

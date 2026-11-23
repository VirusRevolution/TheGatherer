import smtplib

from config.config import config
from email.mime.text        import MIMEText


def send_email(receiver: str, subject: str, content: str) -> bool:
    # Create the email message
    msg            = MIMEText(content)
    msg['Subject'] = subject
    msg['From']    = config.smtp.user
    msg['To']      = receiver

    # Send email
    with smtplib.SMTP(config.email.smtp.host, config.email.smtp.port) as s:
        s.starttls()  # Start TLS encryption
        s.login(config.smtp.user, config.smtp.password)  # Login to SMTP server
        s.sendmail(config.smtp.user, [receiver], msg.as_string())  # Send the email

        return True
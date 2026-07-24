import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_email(to: str, subject: str, html: str) -> None:
    message = EmailMessage()
    message["From"] = settings.EMAIL_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content(html, subtype="html")

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)

        try:
            server.send_message(message)
        except smtplib.SMTPException:
            # TODO: logger
            pass

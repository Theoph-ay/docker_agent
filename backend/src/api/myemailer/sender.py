import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
EMAIL_HOST=os.getenv("EMAIL_HOST") or "smtp.gmail.com"
EMAIL_PORT=os.getenv("EMAIL_PORT") or 465


def send_mail(subject: str="No Subject provided", contents: str ="No Content provided", to_email:str=EMAIL_ADDRESS, from_email:str=EMAIL_ADDRESS):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(contents)
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        return smtp.send_message(msg)
import os
from email.message import EmailMessage

EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
EMAIL_HOST=os.getenv("EMAIL_HOST") or "smtp.gmail.com"
EMAIL_PORT=os.getenv("EMAIL_PORT") or 465


def send_email(subject: str, contents: str, to_email: str, from_email:str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(contents)
    return msg
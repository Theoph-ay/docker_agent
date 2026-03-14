import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
EMAIL_HOST=os.getenv("EMAIL_HOST") or "smtp.gmail.com"
EMAIL_PORT=os.getenv("EMAIL_PORT") or 465


import markdown

def send_mail(subject: str="No Subject provided", contents: str ="No Content provided", to_email:str=EMAIL_ADDRESS, from_email:str=EMAIL_ADDRESS):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    
    # Set the plaintext fallback
    msg.set_content(contents)
    
    # Convert markdown to HTML and add it as an alternative format
    try:
        html_content = markdown.markdown(str(contents), extensions=['tables', 'fenced_code'])
        msg.add_alternative(html_content, subtype='html')
    except Exception as e:
        print(f"Failed to parse Markdown to HTML: {e}")
        
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        return smtp.send_message(msg)
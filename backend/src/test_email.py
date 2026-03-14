from api.myemailer.sender import send_mail
from dotenv import load_dotenv
import os

load_dotenv(".env.sample") # or whichever env file is being used in docker

print("EMAIL_HOST:", os.getenv("EMAIL_HOST"))
print("EMAIL_PORT:", os.getenv("EMAIL_PORT"))
print("EMAIL_ADDRESS:", os.getenv("EMAIL_ADDRESS"))

try:
    send_mail(subject="Test Email", contents="Test from backend debug script", to_email="olayiwolatheophilusayomide@gmail.com")
    print("Email sent successfully!")
except Exception as e:
    print("Error sending email:", e)

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
TO_EMAIL = os.getenv("COUNSELOR_EMAIL")

message = Mail(
    from_email=SENDER_EMAIL,
    to_emails=TO_EMAIL,
    subject="SendGrid Test",
    html_content="<strong>Hello! This is a test email.</strong>"
)

try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print("Status Code:", response.status_code)
except Exception as e:
    print("Error:", e)

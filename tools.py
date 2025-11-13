import os
import logging
from langchain_core.tools import tool
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
COUNSELOR_EMAIL = os.getenv("COUNSELOR_EMAIL")

logging.basicConfig(level=logging.INFO)

@tool
def get_admission_prediction(target_course: str, student_marks: float) -> str:
    """
    Predicts admission probability based on student marks against course-specific cutoffs.
    Returns a string summary.
    """

    # Normalize course name for matching
    course = target_course.strip().lower()

    # Define cutoffs for each course
    course_cutoffs = {
        "cse": 95,
        "computer science and engineering": 95,
        "it": 90,
        "information technology": 90,
        "mechanical": 60,
        "mechanical engineering": 60,
        "entc": 80,
        "electronics and telecommunication engineering": 80,
        "civil": 40,
        "civil engineering": 40,
        "ai": 90,
        "artificial intelligence": 90,
        "b.tech ai": 90,
        "electrical": 50,
        "electrical engineering": 50,
    }

    # Get cutoff or default
    cutoff = course_cutoffs.get(course, 70)

    # Compute probability relative to cutoff
    if student_marks >= cutoff:
        prob = min(1.0, 0.8 + (student_marks - cutoff) / 100)  # High chance
    else:
        diff = cutoff - student_marks
        if diff <= 5:
            prob = 0.6
        elif diff <= 10:
            prob = 0.4
        elif diff <= 20:
            prob = 0.2
        else:
            prob = 0.1

    return f"Prediction Result: Admission chance for {target_course} is {prob*100:.1f}%. Score Value: {prob:.2f}"

@tool
def send_email_alert(subject: str, body: str) -> str:
    """
    Sends a critical alert email to the counselor team.
    """
    if not all([SENDGRID_API_KEY, SENDER_EMAIL, COUNSELOR_EMAIL]):
        logging.error("[EMAIL FAILED] SendGrid configuration missing.")
        return "[EMAIL FAILED] Missing SendGrid configuration."

    try:
        html_body_content = body.replace("\n", "<br>")
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=COUNSELOR_EMAIL,
            subject=subject,
            html_content=f"<strong>{subject}</strong><br><br>{html_body_content}"
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"[EMAIL SENT] Status: {response.status_code}")
        if response.status_code == 202:
            return "Critical Email Alert successfully dispatched via SendGrid."
        else:
            return f"SendGrid API responded with status {response.status_code}"
    except Exception as e:
        logging.error(f"[EMAIL ERROR] {e}")
        return f"Email dispatch failed due to API error: {e}"

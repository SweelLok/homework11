import time


def send_email(email: str, subject: str, body: str):
    time.sleep(2)
    print(f"[EMAIL] To: {email}, Subject: {subject}, Body: {body}")
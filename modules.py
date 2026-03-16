import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from faker import Faker

import config

fake = Faker()


def generate_fake_name():
    """Generate a random fake full name."""
    return fake.name()


def validate_phone(phone):
    """Validate a Sri Lankan phone number (+94XXXXXXXXX)."""
    return bool(re.match(config.PHONE_REGEX, phone))


def validate_email_addr(email):
    """Basic email format validation."""
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def send_sms(phone, message):
    """Send an anonymous SMS via TextBelt API.

    Returns a dict with 'success', 'quotaRemaining', etc.
    """
    if not validate_phone(phone):
        return {"success": False, "error": "Invalid phone number format. Use +94XXXXXXXXX"}

    sender_name = generate_fake_name()
    full_message = f"[From: {sender_name}]\n\n{message}"

    try:
        resp = requests.post(
            config.TEXTBELT_URL,
            data={
                "phone": phone,
                "message": full_message,
                "key": config.TEXTBELT_KEY,
            },
            timeout=30,
        )
        result = resp.json()
        result["sender_name"] = sender_name
        return result
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Network error: {e}", "sender_name": sender_name}


def send_email(to_addr, subject, body):
    """Send an anonymous email via SMTP with a fake sender name.

    Returns (success: bool, sender_name: str, error: str or None).
    """
    cfg = config.smtp_config

    if not cfg["email"] or not cfg["password"]:
        return False, None, "SMTP not configured. Use option [3] to set up SMTP first."

    if not validate_email_addr(to_addr):
        return False, None, "Invalid recipient email address."

    sender_name = generate_fake_name()

    msg = MIMEMultipart()
    msg["From"] = f"{sender_name} <{cfg['email']}>"
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Remove identifying headers
    del msg["X-Mailer"]

    try:
        with smtplib.SMTP(cfg["host"], cfg["port"], timeout=30) as server:
            server.starttls()
            server.login(cfg["email"], cfg["password"])
            server.send_message(msg)
        return True, sender_name, None
    except smtplib.SMTPAuthenticationError:
        return False, sender_name, "Authentication failed. Check your email and app password."
    except smtplib.SMTPException as e:
        return False, sender_name, f"SMTP error: {e}"
    except Exception as e:
        return False, sender_name, f"Error: {e}"

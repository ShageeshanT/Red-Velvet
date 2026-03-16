import os

# TextBelt SMS API
TEXTBELT_URL = "https://textbelt.com/text"
TEXTBELT_KEY = os.environ.get("TEXTBELT_API_KEY", "textbelt")

# Phone validation (Sri Lankan +94 numbers)
PHONE_REGEX = r"^\+94\d{9}$"

# Default SMTP settings
DEFAULT_SMTP_HOST = "smtp.gmail.com"
DEFAULT_SMTP_PORT = 587

# Runtime SMTP config (in-memory only)
smtp_config = {
    "host": DEFAULT_SMTP_HOST,
    "port": DEFAULT_SMTP_PORT,
    "email": None,
    "password": None,
}

DISCLAIMER = """
  Red Velvet - Educational Anonymous Messaging Tool
  --------------------------------------------------
  This tool is designed for EDUCATIONAL and PERSONAL
  TESTING purposes only. Do not use this tool to harass,
  threaten, or spam anyone. The developer assumes no
  responsibility for misuse. Always respect local laws
  and the privacy of others.

  Features:
    - Anonymous SMS to +94 (Sri Lanka) numbers via TextBelt
    - Anonymous Email via SMTP with random sender names
    - Random fake name generation for sender identity

  TextBelt Free Tier: 1 SMS per day
  For more quota, set TEXTBELT_API_KEY environment variable.
"""

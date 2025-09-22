from datetime import datetime, timedelta

import os, smtplib, ssl
from email.mime.text import MIMEText

from fastapi import HTTPException
from jose import jwt, JWTError
from email.message import EmailMessage

MAGIC_LINK_EXPIRE_MINUTES = 15
SECRET_KEY = "h4lgTWGCyht5RA7-heKdOga0jdfX08t7ej3hPVLJ2L4"
ALGORITHM = "HS256"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER ="kpvsraviteja@gmail.com" 
SMTP_PASS ="bpvp xmph gpxi mvcr"
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER or "no-reply@example.com")

def create_magic_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=MAGIC_LINK_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_magic_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token payload")
        return email
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired link")

# === Email helper ===
def send_magic_link(to_email: str, magic_link: str):
    """Send the magic link via SMTP; raise if misconfigured/fails."""
    # Dev fallback: print to console if SMTP not configured
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        print(f"[DEV] Magic link for {to_email}: {magic_link}")
        return

    msg = EmailMessage()
    msg["Subject"] = "Your CloudOU sign-in link"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(
        f"Click to sign in:\n\n{magic_link}\n\n"
        "If you didn’t request this, you can ignore this email."
    )
    msg.add_alternative(
        f"""
        <p>Click to sign in:</p>
        <p><a href="{magic_link}">{magic_link}</a></p>
        <p>If you didn’t request this, you can ignore this email.</p>
        """,
        subtype="html",
    )

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
        server.ehlo()
        # STARTTLS for 587
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

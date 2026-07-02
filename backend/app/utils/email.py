from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from ..schemas.auth import RESET_TOKEN_EXPIRE_MINUTES
import os
from dotenv import load_dotenv
load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    USE_CREDENTIALS = True, 
    VALIDATE_CERTS = True,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False
)

async def send_password_reset_email(email_to: str, token: str):
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"
    
    html = f"""
    <p>Hello bạn,</p>
    <p>Bấm vào link này để reset mật khẩu: <a href="{reset_link}">Reset Password</a></p>
    <p>Link này hết hạn trong {RESET_TOKEN_EXPIRE_MINUTES} phút.</p>
    """
    
    message = MessageSchema(
        subject="Reset mật khẩu App Flashcard",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)
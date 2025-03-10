import os
import bcrypt
import secrets
import jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from custom_exception import BookingError
SECRET_KEY = str(os.getenv('SECRET_KEY'))


def password_to_hash(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed


def verify_password(target_password, hashed):
    return bcrypt.checkpw(target_password.encode('utf-8'), hashed)


def generate_token():
    length = 32
    return secrets.token_hex(length)


def jwt_check(request):
    token = request.headers.get('Authorization')

    if not token:
        raise BookingError(message='Token is missing', status=401)

    token = token.split()[1]

    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    return payload


def send_email(username, email, event):
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT'))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

    subject = 'Thank you for booking!'
    message = f'Dear, {username}! You have booked an event! {event["name"]}, date: {event["date"]}, host:{event["creator"]}!'

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, email, msg.as_string())

            return None

    except Exception as e:
        raise BookingError(message=e, status=500)


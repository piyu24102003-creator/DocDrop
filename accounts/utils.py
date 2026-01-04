from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import string


def generate_random_password(length=12):
    """Generate a secure random password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    # Ensure at least one of each type
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation),
    ]
    # Fill the rest
    password += [random.choice(characters) for _ in range(length - 4)]
    random.shuffle(password)
    return ''.join(password)


def generate_otp(length=6):
    """Generate a 6-digit OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def send_client_welcome_email(user, password, owner):
    """Send welcome email to new client with credentials"""
    subject = 'Welcome to DocDrop - Your Account Details'
    
    context = {
        'user': user,
        'password': password,
        'owner': owner,
        'login_url': settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000'
    }
    
    # Render HTML email
    html_message = render_to_string('emails/client_welcome.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_otp(user, otp):
    """Send OTP for password reset"""
    subject = 'DocDrop - Password Reset OTP'
    
    context = {
        'user': user,
        'otp': otp,
    }
    
    # Render HTML email
    html_message = render_to_string('emails/password_reset_otp.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )

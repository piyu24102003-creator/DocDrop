from django.core.mail import send_mail, get_connection
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


def get_email_connection(owner=None):
    """Get a dynamic email connection based on owner credentials or default settings"""
    if owner and hasattr(owner, 'profile') and owner.profile.smtp_email and owner.profile.smtp_password:
        return get_connection(
            backend=settings.EMAIL_BACKEND,
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=owner.profile.smtp_email,
            password=owner.profile.smtp_password,
            use_tls=settings.EMAIL_USE_TLS,
            fail_silently=False
        )
    return get_connection() # Uses default settings


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
    
    connection = get_email_connection(owner)
    from_email = owner.profile.smtp_email if (owner and hasattr(owner, 'profile') and owner.profile.smtp_email) else settings.DEFAULT_FROM_EMAIL
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
        connection=connection
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

from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docdrop.settings')
django.setup()

User = get_user_model()
username = 'admin'
email = 'admin@docdrop.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    user = User.objects.create_superuser(username, email, password)
    # Ensure profile exists and is marked as admin
    # Depending on signals, profile might be created. Let's check.
    if hasattr(user, 'profile'):
        user.profile.role = 'admin'
        user.profile.save()
        print(f"Superuser {username} created and role set to admin.")
    else:
        # Create profile if not automatic (though models.py usually has signals)
        from accounts.models import UserProfile
        UserProfile.objects.create(user=user, role='admin')
        print(f"Superuser {username} created and profile created manually.")
else:
    print(f"Superuser {username} already exists.")

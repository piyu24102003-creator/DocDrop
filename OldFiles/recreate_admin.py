import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docdrop.settings')
django.setup()

from django.contrib.auth.models import User
try:
    from accounts.models import UserProfile
except ImportError:
    UserProfile = None

def recreate_admin():
    # 1. Remove all old superusers
    superusers = User.objects.filter(is_superuser=True)
    count = superusers.count()
    print(f"Removing {count} existing superusers...")
    superusers.delete()

    # 2. Create new superuser
    username = 'piyu24102003@gmail.com'
    email = 'piyu24102003@gmail.com'
    password = 'piyu@24102003'

    print(f"Creating new superuser: {username}")
    user = User.objects.create_superuser(username=username, email=email, password=password)

    # 3. Ensure profile is set to admin
    if UserProfile:
        # The signal should have created the profile, but we need to set the role
        if hasattr(user, 'profile'):
            user.profile.role = 'admin'
            user.profile.save()
            print("User profile role set to admin.")
        else:
            UserProfile.objects.create(user=user, role='admin')
            print("User profile created and role set to admin.")
    else:
        print("UserProfile model not found, skipping profile update.")

    print("Success! You can now login with:")
    print(f"Username: {username}")
    print(f"Password: {password}")

if __name__ == "__main__":
    recreate_admin()

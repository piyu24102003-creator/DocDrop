import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docdrop.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

with open('admin_list.txt', 'w') as f:
    f.write("--- Administrator Accounts ---\n")
    found_admin = False
    for user in User.objects.all():
        is_superuser = user.is_superuser
        role = 'N/A'
        if hasattr(user, 'profile'):
            role = user.profile.role
        
        if is_superuser or role == 'admin':
            found_admin = True
            f.write(f"USER: {user.username} | EMAIL: {user.email} | SUPERUSER: {is_superuser} | ROLE: {role}\n")

    if not found_admin:
        f.write("No administrator accounts found.\n")

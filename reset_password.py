import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docdrop.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
new_password = 'admin123'

superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    u = superusers.first()
    u.set_password('admin123')
    u.save()
    print(f"Found superuser: {u.username}")
    print(f"Password reset to: admin123")
else:
    print("No superuser found. Creating 'admin'...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created with password 'admin123'")

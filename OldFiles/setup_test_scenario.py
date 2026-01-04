import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docdrop.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def create_firm(email, name, firm_name):
    user, created = User.objects.get_or_create(username=email, email=email)
    if created:
        user.set_password('testpass123')
        user.first_name = name
        user.is_staff = True
        user.save()
    
    profile = user.profile
    profile.role = 'admin'
    profile.firm_name = firm_name
    profile.save()
    print(f"Firm created: {firm_name} ({email})")
    return user

def create_client(email, name, owners):
    user, created = User.objects.get_or_create(username=email, email=email)
    if created:
        user.set_password('testpass123')
        user.first_name = name
        user.save()
    
    profile = user.profile
    profile.role = 'user'
    for owner in owners:
        profile.owners.add(owner)
    profile.save()
    print(f"Client created: {name} ({email}) - Linked to {len(owners)} owners")
    return user

def setup():
    print("Setting up test scenario...")
    
    # Create Owners
    arjun = create_firm("Arjun@gmail.com", "Arjun", "Arjun's Legal Services")
    sahdev = create_firm("Sahdev@gmail.com", "Sahdev", "Sahdev & Co. Auditors")
    
    # Create Clients
    create_client("Abhi@gmail.com", "Abhi", [arjun])
    create_client("Bhim@gmail.com", "Bhim", [arjun, sahdev]) # Linked to both!
    create_client("Chetan@gmail.com", "Chetan", [arjun])
    create_client("Danzo@gmail.com", "Danzo", [sahdev])
    create_client("Emen@gmail.com", "Emen", [sahdev])
    
    print("\nSetup complete!")
    print("All passwords are set to: testpass123")
    print("\nScenario Summary:")
    print("1. Bhim@gmail.com can send documents to both Arjun and Sahdev.")
    print("2. Abhi and Chetan can only send to Arjun.")
    print("3. Danzo and Emen can only send to Sahdev.")

if __name__ == "__main__":
    setup()

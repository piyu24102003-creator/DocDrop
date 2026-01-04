import os
import django
from django.conf import settings
from django.template import Template, Context
from django.template.loader import render_to_string

# Minimal Django configuration for verification
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='verification_key',
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(os.getcwd(), 'templates')],
            'APP_DIRS': False,
            'OPTIONS': {
                'context_processors': [],
            },
        }],
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
    )
    django.setup()

def verify():
    print("Starting minimal verification...")
    try:
        class MockUser:
            def __init__(self, username, first_name='', last_name='', email=''):
                self.username = username
                self.first_name = first_name
                self.last_name = last_name
                self.email = email
                self.profile = type('obj', (object,), {'firm_name': None})
            def get_full_name(self):
                if self.first_name and self.last_name:
                    return f"{self.first_name} {self.last_name}"
                return ""

        user = MockUser(username='testclient@example.com', email='testclient@example.com', first_name='Test', last_name='Client')
        owner = MockUser(username='testowner@example.com', email='testowner@example.com', first_name='Test', last_name='Owner')
        
        context = {
            'user': user,
            'owner': owner,
            'password': 'password123',
            'login_url': 'localhost:8000'
        }
        
        # Load the template file directly to avoid loaders issues in minimal config
        template_path = 'templates/emails/client_welcome.html'
        print(f"Reading template from: {os.path.abspath(template_path)}")
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # print(f"--- Template Content Snippet ---\n{template_content[2000:3000]}\n--------------------------------")

        t = Template(template_content)
        rendered = t.render(Context(context))
        
        # Check for the owner tag part
        search_str = 'Your account has been created by'
        start_idx = rendered.find(search_str)
        if start_idx == -1:
            print("FAILURE: Could not find the expected sentence in rendered output.")
            return

        end_idx = rendered.find('. You can now', start_idx)
        if end_idx == -1:
            print("FAILURE: Could not find the end of the sentence in rendered output.")
            return
            
        snippet = rendered[start_idx:end_idx].strip()
        print(f"--- Rendered Content Snippet ---\n{snippet}\n---------------------------------")
        
        if '{{' in rendered or '{%' in rendered:
            print("FAILURE: Found unrendered tags!")
            tag_idx = rendered.find('{{')
            if tag_idx != -1:
                print(f"Unrendered tag found around: {rendered[tag_idx:tag_idx+50]}")
        elif 'Test Owner' in snippet or 'testowner' in snippet:
            print("SUCCESS: Owner name rendered correctly.")
        else:
            print(f"FAILURE: Owner name not found in snippet. Found: '{snippet}'")
            
    except Exception as e:
        print(f"ERROR during verification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify()

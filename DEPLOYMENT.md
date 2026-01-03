# Deployment Guide - PythonAnywhere

This guide provides step-by-step instructions for deploying DocDrop to PythonAnywhere.

## Prerequisites

- PythonAnywhere account (free tier available)
- GitHub repository with your code
- Email credentials for Gmail SMTP

## Step 1: Create PythonAnywhere Account

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/)
2. Sign up for a free Beginner account
3. Verify your email address

## Step 2: Set Up MySQL Database

1. Go to **Databases** tab in PythonAnywhere dashboard
2. Set a MySQL password (remember this!)
3. Create a new database:
   - Database name: `yourusername$docdrop` (e.g., `deepb$docdrop`)
4. Note your database details:
   - Host: `yourusername.mysql.pythonanywhere-services.com`
   - Username: `yourusername`
   - Database: `yourusername$docdrop`

## Step 3: Clone Your Repository

1. Go to **Consoles** tab
2. Start a **Bash console**
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/DocDrop.git
   cd DocDrop/docdrop
   ```

## Step 4: Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 docdrop-env
workon docdrop-env
pip install -r requirements.txt
```

## Step 5: Configure Environment Variables

1. Create `.env` file in the `docdrop` directory:
   ```bash
   cd ~/DocDrop/docdrop
   nano .env
   ```

2. Add your environment variables:
   ```bash
   SECRET_KEY=your-generated-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourusername.pythonanywhere.com
   DATABASE_URL=mysql://yourusername:your_mysql_password@yourusername.mysql.pythonanywhere-services.com/yourusername$docdrop
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   DEFAULT_FROM_EMAIL=DocDrop <your-email@gmail.com>
   ```

3. Save and exit (Ctrl+X, then Y, then Enter)

### Generate a Secret Key

Run this in the console:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 6: Run Database Migrations

```bash
cd ~/DocDrop/docdrop
python manage.py migrate
```

## Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 8: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Step 9: Configure Web App

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Django wizard)
4. Select **Python 3.10**

### Configure Source Code

- Source code: `/home/yourusername/DocDrop/docdrop`
- Working directory: `/home/yourusername/DocDrop/docdrop`

### Configure Virtual Environment

- Virtualenv: `/home/yourusername/.virtualenvs/docdrop-env`

### Configure WSGI File

1. Click on the WSGI configuration file link
2. Delete all content and replace with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/DocDrop/docdrop'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'docdrop.settings'

# Load environment variables from .env file
from pathlib import Path
import environ

BASE_DIR = Path('/home/yourusername/DocDrop/docdrop')
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. Replace `yourusername` with your actual PythonAnywhere username
4. Save the file

### Configure Static Files

In the **Web** tab, add static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/DocDrop/docdrop/staticfiles` |
| `/media/` | `/home/yourusername/DocDrop/docdrop/media` |

Replace `yourusername` with your actual username.

## Step 10: Reload Web App

1. Go back to the **Web** tab
2. Click the green **Reload** button
3. Wait for the reload to complete

## Step 11: Test Your Application

1. Visit `https://yourusername.pythonanywhere.com`
2. Test the following:
   - Homepage loads correctly
   - User registration works
   - Login functionality
   - Document upload (as owner)
   - Client access

## Troubleshooting

### Error Logs

View error logs in the **Web** tab:
- Error log: Shows Python errors
- Server log: Shows HTTP requests
- Access log: Shows all requests

### Common Issues

**1. ImportError or Module Not Found**
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

**2. Database Connection Error**
- Verify DATABASE_URL in `.env`
- Check MySQL password is correct
- Ensure database exists

**3. Static Files Not Loading**
- Run `python manage.py collectstatic --noinput`
- Check static file mappings in Web tab
- Verify STATIC_ROOT path

**4. Email Not Sending**
- Verify Gmail App Password (not regular password)
- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in `.env`
- Enable "Less secure app access" or use App Password

**5. 500 Internal Server Error**
- Check error log in Web tab
- Verify all environment variables are set
- Ensure DEBUG=False in production

### Updating Your Application

When you make changes to your code:

```bash
cd ~/DocDrop
git pull origin main
workon docdrop-env
pip install -r docdrop/requirements.txt  # If dependencies changed
cd docdrop
python manage.py migrate  # If models changed
python manage.py collectstatic --noinput  # If static files changed
```

Then reload your web app from the Web tab.

## Security Checklist

- ✅ DEBUG=False in production
- ✅ SECRET_KEY is unique and secret
- ✅ ALLOWED_HOSTS configured correctly
- ✅ Database password is strong
- ✅ Email credentials are secure (use App Password)
- ✅ .env file is not in Git repository
- ✅ HTTPS is enabled (automatic on PythonAnywhere)

## Performance Tips

1. **Free Tier Limitations**:
   - App sleeps after inactivity
   - Limited CPU seconds per day
   - One web app only

2. **Optimize**:
   - Use WhiteNoise for static files (already configured)
   - Keep media files small
   - Monitor CPU usage in dashboard

## Alternative Deployment Platforms

If you need more resources or features:

### Render
- Free tier available
- Automatic deployments from GitHub
- PostgreSQL database included
- See `render.yaml` in project root

### Railway
- Free tier with credits
- Easy deployment
- PostgreSQL support

### Heroku
- Free tier discontinued
- Paid plans available
- Good documentation

## Support

For deployment issues:
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- PythonAnywhere Help: https://help.pythonanywhere.com/

For application issues:
- Contact: deepbuhecha7@gmail.com

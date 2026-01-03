# DocDrop - Installation & Setup Guide

## Complete Installation Documentation

**Version:** 1.0.0  
**Last Updated:** January 2, 2026  
**Difficulty:** Beginner to Intermediate

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Email Configuration](#email-configuration)
6. [Running the Application](#running-the-application)
7. [Creating Admin Account](#creating-admin-account)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

#### Operating System
- **Windows**: Windows 10 or later
- **macOS**: macOS 10.14 (Mojave) or later
- **Linux**: Ubuntu 18.04+ / Debian 10+ / CentOS 7+

#### Software Requirements
- **Python**: 3.8 or higher (3.10+ recommended)
- **pip**: Latest version (comes with Python)
- **Git**: For version control (optional but recommended)
- **Tesseract OCR**: For document text extraction

#### Hardware Requirements
```
Minimum:
- RAM: 4GB
- Storage: 2GB free space
- Processor: Dual-core 2.0 GHz

Recommended:
- RAM: 8GB or more
- Storage: 10GB+ free space (SSD preferred)
- Processor: Quad-core 2.5 GHz+
```

### Installing Prerequisites

#### Windows

**1. Install Python**
```powershell
# Download from python.org
# OR use Windows Store
# OR use Chocolatey
choco install python --version=3.10.11
```

**2. Install Tesseract OCR**
```powershell
# Download installer from:
# https://github.com/UB-Mannheim/tesseract/wiki

# OR use Chocolatey
choco install tesseract

# Add to PATH:
# C:\Program Files\Tesseract-OCR
```

**3. Install Git (Optional)**
```powershell
# Download from git-scm.com
# OR use Chocolatey
choco install git
```

#### macOS

**1. Install Homebrew** (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install Python**
```bash
brew install python@3.10
```

**3. Install Tesseract OCR**
```bash
brew install tesseract
```

**4. Install Git**
```bash
brew install git
```

#### Linux (Ubuntu/Debian)

**1. Update Package List**
```bash
sudo apt update
```

**2. Install Python**
```bash
sudo apt install python3.10 python3-pip python3-venv
```

**3. Install Tesseract OCR**
```bash
sudo apt install tesseract-ocr
```

**4. Install Git**
```bash
sudo apt install git
```

### Verify Installation

```bash
# Check Python version
python --version
# Should show: Python 3.10.x or higher

# Check pip version
pip --version
# Should show: pip 23.x.x or higher

# Check Tesseract
tesseract --version
# Should show: tesseract 4.x.x or higher

# Check Git
git --version
# Should show: git version 2.x.x or higher
```

---

## Installation Steps

### Step 1: Download Project

#### Option A: Using Git (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd DocDrop
```

#### Option B: Download ZIP
1. Download project ZIP file
2. Extract to desired location
3. Open terminal/command prompt in extracted folder

### Step 2: Create Virtual Environment

A virtual environment isolates project dependencies from system Python.

#### Windows
```powershell
# Navigate to project directory
cd DocDrop

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your prompt
```

#### macOS/Linux
```bash
# Navigate to project directory
cd DocDrop

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

**Important**: Always activate the virtual environment before working on the project!

### Step 3: Install Dependencies

```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Navigate to Django project directory
cd docdrop

# Install required packages
pip install -r requirements.txt

# This will install:
# - Django 6.0
# - Pillow (image processing)
# - pytesseract (OCR)
# - django-environ (environment variables)
# - whitenoise (static files)
```

**Verify Installation**:
```bash
pip list
# Should show all installed packages
```

### Step 4: Environment Configuration

#### Create .env File

The `.env` file stores sensitive configuration. **Never commit this file to Git!**

**Windows**:
```powershell
# In docdrop/ directory
copy .env.example .env
```

**macOS/Linux**:
```bash
# In docdrop/ directory
cp .env.example .env
```

#### Edit .env File

Open `.env` in a text editor and configure:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration (Gmail)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=DocDrop <your-email@gmail.com>
```

**Important Configuration Notes**:

1. **SECRET_KEY**: 
   - For development, you can use the default
   - For production, generate a new one:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **DEBUG**:
   - `True` for development (shows detailed errors)
   - `False` for production (security)

3. **EMAIL_HOST_PASSWORD**:
   - **NOT** your regular Gmail password
   - Use Gmail App Password (see Email Configuration section)

---

## Database Setup

### Step 1: Apply Migrations

Migrations create the database tables.

```bash
# Make sure you're in docdrop/ directory
# And virtual environment is activated

# Create migration files (if needed)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# You should see:
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   Applying accounts.0001_initial... OK
#   ... (more migrations)
```

**What This Does**:
- Creates `db.sqlite3` file in docdrop/ directory
- Creates all necessary database tables
- Sets up Django's built-in tables (auth, sessions, etc.)
- Creates custom tables (UserProfile, Document, DocumentRequest, etc.)

### Step 2: Create Superuser (Optional)

A superuser has access to Django admin panel.

```bash
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@example.com
# Password: ******** (min 8 characters)
# Password (again): ********
```

**Note**: This is different from Owner accounts. Superuser is for Django admin panel only.

### Step 3: Verify Database

```bash
# Check database tables
python manage.py dbshell

# In SQLite shell:
.tables
# Should show: accounts_userprofile, documents_document, etc.

# Exit shell:
.exit
```

---

## Email Configuration

### Gmail App Password Setup

**Why App Password?**
- Gmail blocks "less secure apps" by default
- App passwords allow applications to send email securely
- More secure than using your regular password

**Steps to Create App Password**:

1. **Enable 2-Step Verification**
   - Go to: https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow setup wizard
   - **Required** for app passwords

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other (Custom name)"
   - Enter name: "DocDrop"
   - Click "Generate"
   - **Copy the 16-character password** (e.g., "abcd efgh ijkl mnop")

3. **Add to .env File**
   ```env
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop  # Remove spaces
   DEFAULT_FROM_EMAIL=DocDrop <your-email@gmail.com>
   ```

### Test Email Configuration

Create a test script `test_email.py` in docdrop/ directory:

```python
# test_email.py
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject='DocDrop Test Email',
    message='If you receive this, email configuration is working!',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['your-email@gmail.com'],
    fail_silently=False,
)
print("Email sent successfully!")
```

Run the test:
```bash
python manage.py shell < test_email.py
```

Check your email inbox. If you receive the test email, configuration is correct!

---

## Running the Application

### Development Server

```bash
# Make sure you're in docdrop/ directory
# And virtual environment is activated

# Start development server
python manage.py runserver

# You should see:
# Watching for file changes with StatReloader
# Performing system checks...
# System check identified no issues (0 silenced).
# January 02, 2026 - 10:15:36
# Django version 6.0, using settings 'docdrop.settings'
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CTRL-BREAK.
```

### Access the Application

Open your web browser and navigate to:
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Owner Login**: http://127.0.0.1:8000/accounts/admin/login/
- **Client Login**: http://127.0.0.1:8000/accounts/login/

### Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.

---

## Creating Admin Account

### Method 1: Owner Registration (Recommended)

1. Go to: http://127.0.0.1:8000/accounts/register/owner/
2. Fill in the registration form:
   - Full Name
   - Firm/Company Name
   - Email (will be username)
   - Contact Number
   - Designation
   - Password (min 8 characters)
   - Confirm Password
3. Click "Register"
4. Login at: http://127.0.0.1:8000/accounts/admin/login/

### Method 2: Using Management Command

Create `create_owner.py` in docdrop/ directory:

```python
# create_owner.py
from django.contrib.auth.models import User

# Create owner account
user = User.objects.create_user(
    username='owner@example.com',
    email='owner@example.com',
    password='password123',
    first_name='John Doe'
)
user.is_staff = True
user.save()

# Update profile
user.profile.role = 'admin'
user.profile.firm_name = 'Example Firm'
user.profile.phone = '1234567890'
user.profile.save()

print(f"Owner account created: {user.username}")
```

Run the script:
```bash
python manage.py shell < create_owner.py
```

---

## Troubleshooting

### Common Issues

#### 1. "python: command not found"

**Problem**: Python not installed or not in PATH

**Solution**:
- **Windows**: Reinstall Python, check "Add Python to PATH"
- **macOS/Linux**: Use `python3` instead of `python`

#### 2. "No module named 'django'"

**Problem**: Virtual environment not activated or Django not installed

**Solution**:
```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. "OperationalError: no such table"

**Problem**: Database migrations not applied

**Solution**:
```bash
python manage.py migrate
```

#### 4. "CSRF verification failed"

**Problem**: CSRF token missing or invalid

**Solution**:
- Clear browser cookies
- Ensure `{% csrf_token %}` is in forms
- Check ALLOWED_HOSTS in settings

#### 5. "SMTPAuthenticationError"

**Problem**: Email credentials incorrect

**Solution**:
- Verify EMAIL_HOST_USER is correct
- Use App Password, not regular password
- Enable 2-Step Verification on Gmail
- Remove spaces from app password

#### 6. "Tesseract not found"

**Problem**: Tesseract OCR not installed or not in PATH

**Solution**:
- **Windows**: Add `C:\Program Files\Tesseract-OCR` to PATH
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt install tesseract-ocr`

#### 7. "Port 8000 already in use"

**Problem**: Another process using port 8000

**Solution**:
```bash
# Use different port
python manage.py runserver 8080

# OR kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

#### 8. "Permission denied" on media files

**Problem**: Incorrect file permissions

**Solution**:
```bash
# macOS/Linux:
chmod -R 755 media/

# Windows: Right-click media folder → Properties → Security
```

### Getting Help

If you encounter issues not covered here:

1. **Check Django Documentation**: https://docs.djangoproject.com/
2. **Check Error Logs**: Look in terminal output
3. **Enable Debug Mode**: Set `DEBUG=True` in .env
4. **Check Browser Console**: F12 → Console tab
5. **Search Stack Overflow**: Most errors are documented

### Useful Commands

```bash
# Check Django version
python -m django --version

# Check installed packages
pip list

# Check for missing migrations
python manage.py showmigrations

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic

# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Open database shell
python manage.py dbshell
```

---

## Next Steps

After successful installation:

1. ✅ **Test the Application**
   - Register as owner
   - Create a client
   - Upload a document
   - Create a document request

2. ✅ **Configure Email**
   - Test email sending
   - Verify client welcome emails
   - Test password reset OTP

3. ✅ **Customize**
   - Update firm name
   - Add logo (future)
   - Customize email templates

4. ✅ **Read User Guide**
   - Learn all features
   - Understand workflows
   - Best practices

5. ✅ **Plan Deployment**
   - Choose hosting platform
   - Configure production settings
   - Set up backups

---

**Installation Complete!** 🎉

You now have a fully functional DocDrop installation. Proceed to the User Guide to learn how to use all features.

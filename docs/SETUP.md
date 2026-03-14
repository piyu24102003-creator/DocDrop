# DocDrop Setup Guide

## Quick Start

### 1. Database Setup

1. Start XAMPP Control Panel
2. Start MySQL service
3. Open phpMyAdmin (http://localhost/phpmyadmin)
4. Create database:
   ```sql
   CREATE DATABASE docdrop_db;
   ```

### 2. Install Dependencies

```bash
# Activate virtual environment
# Windows
# or
source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 3. Configure Database (if needed)

The database is already configured for XAMPP default (no password). If you have a MySQL password, edit `docdrop/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'docdrop_db',
        'USER': 'root',
        'PASSWORD': '',  # Update if you have a password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

**Note**: The project uses PyMySQL for MySQL connectivity (works better on Windows/XAMPP).

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

### 6. Set Admin Role

1. Run server: `python manage.py runserver`
2. Go to http://127.0.0.1:8000/admin/
3. Login with superuser credentials
4. Go to "User profiles"
5. Find your user and set Role to "Admin"
6. Save

### 7. Start Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Creating Regular Users

### Option 1: Via Admin Panel (Web Interface)
1. Login as admin
2. Click "Users" in navigation
3. Click "Create User"
4. Fill in details and select role
5. User can now login

### Option 2: Via Django Admin
1. Go to http://127.0.0.1:8000/admin/
2. Go to "Users"
3. Click "Add user"
4. Create user and set password
5. Go to "User profiles" and set role

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL is running in XAMPP
- Check database name matches in settings.py
- Verify MySQL password is correct

### Migration Errors
- If you get "table already exists" errors, run: `python reset_db.py` (this will drop and recreate the database)
- Then run: `python manage.py migrate` again
- Make sure MySQL is running in XAMPP before running migrations

### Static Files Not Loading
- Run: `python manage.py collectstatic` (for production)
- Ensure DEBUG = True in settings.py (for development)

### Media Files Not Accessing
- Ensure media/ directory exists in project root
- Check MEDIA_URL and MEDIA_ROOT in settings.py

## Default URLs

- Home/Login: http://127.0.0.1:8000/
- Admin Dashboard: http://127.0.0.1:8000/admin/dashboard/
- User Dashboard: http://127.0.0.1:8000/user/dashboard/
- Django Admin: http://127.0.0.1:8000/admin/

## File Upload Limits

- Maximum file size: 10MB
- Allowed formats: JPG, JPEG, PNG, PDF, DOC, DOCX
- Files stored in: `media/documents/username/`


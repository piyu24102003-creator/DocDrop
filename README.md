# DocDrop - Document Management System

A secure web-based document sharing and management application built with Django.

## Features

### 🔐 Authentication
- Secure login/logout
- Role-based access control (Admin/User)
- Email-based password reset
- Session management

### 📁 Document Management
- Upload documents (JPG, PNG, PDF, DOC, DOCX)
- View uploaded documents
- Download documents
- Delete documents
- File size validation (10MB max)
- File type validation

### 📊 Dashboards

#### Admin Dashboard
- Total users and documents statistics
- Recent uploads
- User-wise document list
- User management (Create, View, Delete)
- View all documents

#### User Dashboard
- Personal document list
- Upload status
- Profile management

## Technology Stack

- **Backend**: Python 3, Django 6.0
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: MySQL (via XAMPP)
- **Storage**: Local storage (development), Cloud storage ready (production)

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server (XAMPP recommended)
- Virtual environment (recommended)

### Step 1: Database Setup

1. Start XAMPP and ensure MySQL is running
2. Create a database:
   ```sql
   CREATE DATABASE docdrop_db;
   ```

### Step 2: Install Dependencies

```bash
# Activate virtual environment (if using)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Configure Settings

Edit `docdrop/settings.py` and update MySQL credentials if needed:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'docdrop_db',
        'USER': 'root',
        'PASSWORD': '',  # Your MySQL password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### Step 4: Run Migrations

```bash
cd docdrop
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. After creation, you can:
1. Login to Django admin panel
2. Go to User Profiles
3. Set the role to "Admin" for your superuser

### Step 6: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Usage

### Creating Users

1. Login as admin
2. Navigate to "Users" in the admin panel
3. Click "Create User"
4. Fill in user details and select role
5. User can now login and upload documents

### Uploading Documents

1. Login as a user
2. Click "Upload Document"
3. Select file (JPG, PNG, PDF, DOC, DOCX)
4. Optionally provide a document name
5. Click "Upload Document"

### Admin Features

- View all users and their documents
- Download any user's documents
- Create/Delete users
- View statistics and recent uploads

## Project Structure

```
docdrop/
├── docdrop/              # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/             # Authentication & User Management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── documents/            # Document Management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── docs/                 # Project documentation
├── templates/            # HTML Templates
│   ├── base/
│   ├── auth/
│   ├── admin/
│   ├── user/
│   └── documents/
├── static/               # Static Files
│   ├── css/
│   └── js/
├── media/                # Uploaded Files
└── manage.py
```

## Security Features

- CSRF protection
- Secure file validation
- Role-based access control
- Password hashing
- Email verification tokens
- Secure media access

## Email Configuration (Password Reset)

For production, update email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

Currently set to console backend for development (emails print to console).

## Future Enhancements

- Camera capture for document upload
- Cloud storage integration (AWS S3 / Cloudinary)
- Advanced search and filtering
- Document preview
- Bulk upload
- Email notifications

## License

This project is for educational purposes.

## Support

For issues or questions, please refer to the Django documentation or create an issue in the repository.


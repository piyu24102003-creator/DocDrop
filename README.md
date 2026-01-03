# DocDrop - Document Management System

A secure, user-friendly document management system built with Django that enables document owners to manage and share documents with clients efficiently.

## Features

### For Document Owners
- **User Registration & Authentication**: Secure signup/login with email verification
- **Document Management**: Upload, organize, and manage documents
- **Client Management**: Add clients and control their document access
- **Access Control**: Grant or revoke client access to specific documents
- **Dashboard**: Comprehensive overview of documents and client activities
- **Password Reset**: Secure OTP-based password recovery via email

### For Clients
- **Secure Access**: Login with credentials provided by document owners
- **Document Viewing**: Browse and download assigned documents
- **User-Friendly Interface**: Clean, responsive design for easy navigation
- **Mobile Support**: Fully responsive for desktop and mobile devices

### Security Features
- Email-based OTP verification for password resets
- Secure file storage and access control
- CSRF protection and secure session management
- Environment-based configuration for sensitive data

## Technology Stack

- **Backend**: Django 6.0
- **Database**: MySQL (via PyMySQL)
- **Frontend**: HTML, CSS, JavaScript (responsive design)
- **File Handling**: Pillow for image processing
- **Static Files**: WhiteNoise for production serving
- **Deployment**: Gunicorn WSGI server

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL database server
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DocDrop
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd docdrop
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the values in `.env`:
     ```bash
     SECRET_KEY=your-generated-secret-key
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1
     DATABASE_URL=mysql://root:password@localhost:3306/docdrop
     EMAIL_HOST_USER=your-email@gmail.com
     EMAIL_HOST_PASSWORD=your-app-password
     DEFAULT_FROM_EMAIL=DocDrop <your-email@gmail.com>
     ```

5. **Create database**
   ```sql
   CREATE DATABASE docdrop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Open browser: `http://localhost:8000`

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for PythonAnywhere and other platforms.

## Project Structure

```
DocDrop/
├── docdrop/                 # Main Django project
│   ├── accounts/           # User authentication & management
│   ├── documents/          # Document management
│   ├── docdrop/           # Project settings
│   ├── templates/         # HTML templates
│   ├── static/            # Static files (CSS, JS, images)
│   ├── media/             # User-uploaded files
│   ├── manage.py          # Django management script
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment variables template
├── Documents/             # Documentation files
└── README.md             # This file
```

## Usage

### For Document Owners

1. **Register**: Create an account from the homepage
2. **Login**: Access your dashboard
3. **Upload Documents**: Add documents to your collection
4. **Add Clients**: Create client accounts
5. **Assign Documents**: Grant clients access to specific documents
6. **Manage Access**: Revoke or modify client permissions as needed

### For Clients

1. **Receive Credentials**: Get login credentials from document owner
2. **Login**: Access your assigned documents
3. **Download**: View and download documents shared with you

## Email Configuration

For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in `EMAIL_HOST_PASSWORD`

## Contributing

This is a private project. For issues or suggestions, please contact the project owner.

## License

All rights reserved. This project is proprietary software.

## Support

For support or questions, please contact: deepbuhecha7@gmail.com

## Acknowledgments

Built with Django and modern web technologies for secure document management.

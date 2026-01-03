# DocDrop

DocDrop is a Django-based web application for managing document uploads, sharing, and email notifications. It provides user authentication, document handling, and email workflows.

## Features
- User registration and login
- Document upload with optional email notifications
- Password reset via OTP
- Admin interface for managing documents

## Setup
1. Clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file (see `.env.example`).
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Deployment
See the `pa_config.sh` script for deployment steps on PythonAnywhere.

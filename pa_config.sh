#!/bin/bash
# pa_config.sh - Setup script for deploying DocDrop on PythonAnywhere

# Exit on any error
set -e

# Navigate to project directory (assumes the repo is cloned into ~/DocDrop)
cd ~/DocDrop

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

# Activate virtualenv
source venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create .env file if missing (prompt user to fill values)
if [ ! -f ".env" ]; then
  cat <<EOF > .env
# Django secret key
SECRET_KEY=your-secret-key

# Debug mode (False for production)
DEBUG=False

# Allowed hosts (add your PythonAnywhere domain)
ALLOWED_HOSTS=your-username.pythonanywhere.com

# Database URL (PythonAnywhere provides MySQL)
# Example format: mysql://username:password@hostname:3306/dbname
DATABASE_URL=mysql://your-db-user:your-db-pass@your-db-host:3306/your-db-name

# Email settings (if using SMTP)
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
EOF
  echo "Created .env template. Please edit it with your actual credentials."
fi

# Deactivate virtualenv
deactivate

echo "Setup complete. You can now reload the web app from the PythonAnywhere dashboard."

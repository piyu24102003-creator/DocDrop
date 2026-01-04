#!/bin/bash
# pa_config.sh - Setup script for deploying DocDrop on PythonAnywhere
# This script should be run from inside the 'docdrop' subfolder

set -e

echo "Starting deployment setup..."

# 1. Setup Virtualenv
if [ ! -d "venv" ]; then
  echo "Creating virtualenv..."
  python3.13 -m venv venv
fi

source venv/bin/activate
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 2. Setup .env if missing
if [ ! -f ".env" ]; then
  echo "Creating .env template..."
  cat <<EOF > .env
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')
DEBUG=False
ALLOWED_HOSTS=buhechapriyanshu24.pythonanywhere.com
DATABASE_URL=mysql://buhechapriyanshu24:YOUR_PASSWORD@buhechapriyanshu24.mysql.pythonanywhere-services.com/buhechapriyanshu24\$default
# Email Settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
EOF
  echo "!!! Action Required: Edit 'docdrop/.env' with your actual MySQL password and email settings !!!"
  echo "!!! (If you don't need email yet, you can leave the email fields as they are) !!!"
fi

# 3. Static Files and Migrations
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete. Next steps:"
echo "1. Edit 'docdrop/.env' and set your database password."
echo "2. Run 'source venv/bin/activate && python manage.py migrate' in this folder."
echo "3. Update your PythonAnywhere Web tab as per the instructions."

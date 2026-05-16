#!/bin/bash

# Exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p static/images
mkdir -p media

# Run migrations
python manage.py migrate --settings=hamrophysio.settings.production

# Collect static files - THIS IS CRITICAL FOR IMAGES
python manage.py collectstatic --noinput --settings=hamrophysio.settings.production

# Verify static files were collected
ls -la staticfiles/
ls -la static/

#!/bin/bash

echo "Starting build..."

pip install --upgrade pip
pip install -r requirements.txt

# Create directories
mkdir -p staticfiles
mkdir -p static/images
mkdir -p media

# Copy images to static folder if they exist elsewhere
if [ -d "static/images" ]; then
    echo "✅ Images found in static/images/"
    ls -la static/images/
fi

# Run migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files (this copies images to staticfiles)
python manage.py collectstatic --noinput --verbosity 2

echo "Build complete!"

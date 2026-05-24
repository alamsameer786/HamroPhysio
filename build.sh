#!/bin/bash

echo "🚀 Starting build process..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Creating directories..."
mkdir -p staticfiles
mkdir -p static/images
mkdir -p core/templates

echo "🗄️ Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!"

import os
import dj_database_url
from .base import *

# Security Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-key')
DEBUG = False

ALLOWED_HOSTS = [
    'hamrophysio.onrender.com',
    'www.hamrophysio.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Database Configuration
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Static Files Configuration - CRITICAL FOR IMAGES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# WhiteNoise Configuration for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security Headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://hamrophysio.onrender.com',
    'https://www.hamrophysio.onrender.com',
]

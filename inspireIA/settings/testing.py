"""
Testing settings for inspireIA project.
"""
import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# For testing, we use a consistent key
SECRET_KEY = 'django-insecure-testing-key-not-for-production'

# Enable debug for easier troubleshooting in tests
DEBUG = True

# Allow localhost and testserver for testing
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# Use in-memory SQLite for faster testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable password hashing to speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable migrations to speed up tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Use console email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configure logging for testing
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
            'propagate': False,
        },
    },
}

# Use the CustomUser model
AUTH_USER_MODEL = 'users.CustomUser'

# Disable CSRF for testing API endpoints
MIDDLEWARE = [m for m in MIDDLEWARE if 'CsrfViewMiddleware' not in m]

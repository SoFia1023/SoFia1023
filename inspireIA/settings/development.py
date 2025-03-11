"""
Development settings for inspireIA project.
"""
from typing import Dict, Any, List
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# In development, we use a hardcoded key, but it can be overridden via .env
SECRET_KEY = get_env_value('DJANGO_SECRET_KEY', 'django-insecure-6)gdd^&=840x=7@6yd7+47m-mi3q+fjg55xd%nyhhk8d-h__@2')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_value('DEBUG', 'True').lower() in ('true', 't', 'yes', 'y', '1')

# Allow localhost and other development hosts
ALLOWED_HOSTS = get_env_value('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Additional development-specific apps
DEBUG_APPS: List[str] = []

# Add Django Debug Toolbar if installed and enabled
if get_env_value('ENABLE_DEBUG_TOOLBAR', 'False').lower() in ('true', 't', 'yes', 'y', '1'):
    try:
        import debug_toolbar
        DEBUG_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1']
    except ImportError:
        pass

INSTALLED_APPS += DEBUG_APPS

# Show emails in the console by default in development
EMAIL_BACKEND = get_env_value(
    'EMAIL_BACKEND', 
    'django.core.mail.backends.console.EmailBackend'
)

# Configure logging for development
LOGGING: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': get_env_value('ROOT_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': get_env_value('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': get_env_value('DB_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        },
    },
}

# API Keys for development (override in .env for your own keys)
OPENAI_API_KEY = get_env_value('OPENAI_API_KEY', '')
HUGGINGFACE_API_KEY = get_env_value('HUGGINGFACE_API_KEY', '')

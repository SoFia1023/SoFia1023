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
# Development-specific logging configuration that overrides base settings
LOGGING: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)-8s%(reset)s %(blue)s[%(asctime)s]%(reset)s %(white)s%(message)s%(reset)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        },
        'verbose': {
            'format': '[{asctime}] {levelname} {module} {process:d} {thread:d} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'formatter': 'verbose',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,
        },
    },
    'root': {
        'handlers': ['console', 'file_debug'],
        'level': get_env_value('ROOT_LOG_LEVEL', 'DEBUG'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_debug'],
            'level': get_env_value('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'file_debug'],
            'level': get_env_value('DB_LOG_LEVEL', 'INFO'),  # Set to DEBUG to log all SQL queries
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Application loggers with more verbose output in development
        'inspireIA': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'catalog': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'users': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'interaction': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'api': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# API Keys should be stored in environment variables only
# Do not store API keys in settings files

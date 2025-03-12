"""
Production settings for inspireIA project.
"""
from typing import Dict, Any, List, Optional, cast
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_value('DJANGO_SECRET_KEY', None)
if not SECRET_KEY:
    raise ValueError(
        "DJANGO_SECRET_KEY environment variable is required in production. "
        "Please set it in your .env file or server environment."
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_value('DEBUG', 'False').lower() in ('true', 't', 'yes', 'y', '1')

# Hosts that can serve the application
ALLOWED_HOSTS = get_env_value('ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError(
        "ALLOWED_HOSTS environment variable is required in production. "
        "Please set it in your .env file or server environment."
    )

# Security settings
SECURE_HSTS_SECONDS = int(get_env_value('SECURE_HSTS_SECONDS', 31536000))  # 1 year default
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_env_value('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() in ('true', 't', 'yes', 'y', '1')
SECURE_HSTS_PRELOAD = get_env_value('SECURE_HSTS_PRELOAD', 'True').lower() in ('true', 't', 'yes', 'y', '1')

# SSL settings
DISABLE_SSL = get_env_value('DISABLE_SSL', 'False').lower() in ('true', 't', 'yes', 'y', '1')
SECURE_SSL_REDIRECT = not DISABLE_SSL
SESSION_COOKIE_SECURE = not DISABLE_SSL
CSRF_COOKIE_SECURE = not DISABLE_SSL

# Additional security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = get_env_value('X_FRAME_OPTIONS', 'DENY')

# Database configuration
# Use environment variables for database configuration in production
DATABASE_URL = get_env_value('DATABASE_URL', None)
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(
                conn_max_age=int(get_env_value('DB_CONN_MAX_AGE', 600)),
                conn_health_checks=get_env_value('DB_CONN_HEALTH_CHECKS', 'True').lower() in ('true', 't', 'yes', 'y', '1'),
            )
        }
    except ImportError:
        raise ImportError(
            "The dj-database-url package is required when using DATABASE_URL. "
            "Install it with: pip install dj-database-url"
        )

# Static and media files
# Configure AWS S3 or other storage backend if needed
USE_S3 = get_env_value('USE_S3', 'False').lower() in ('true', 't', 'yes', 'y', '1')
if USE_S3:
    # Validate required S3 settings
    required_s3_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_STORAGE_BUCKET_NAME']
    missing_vars = [var for var in required_s3_vars if not get_env_value(var)]
    if missing_vars:
        raise ValueError(f"Missing required S3 environment variables: {', '.join(missing_vars)}")
    
    # AWS settings
    AWS_ACCESS_KEY_ID = get_env_value('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = get_env_value('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = get_env_value('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = get_env_value('AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')
    AWS_S3_OBJECT_PARAMETERS: Dict[str, Any] = {
        'CacheControl': f"max-age={get_env_value('AWS_S3_CACHE_MAX_AGE', 86400)}",
    }
    
    # S3 static settings
    STATIC_LOCATION = get_env_value('STATIC_LOCATION', 'static')
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'inspireIA.storage_backends.StaticStorage'
    
    # S3 media settings
    MEDIA_LOCATION = get_env_value('MEDIA_LOCATION', 'media')
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'inspireIA.storage_backends.MediaStorage'
else:
    # Local storage
    STATIC_URL = get_env_value('STATIC_URL', '/static/')
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = get_env_value('MEDIA_URL', '/media/')
    MEDIA_ROOT = BASE_DIR / 'media'

# Email configuration
EMAIL_BACKEND = get_env_value('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = get_env_value('EMAIL_HOST')
EMAIL_PORT = int(get_env_value('EMAIL_PORT', 587))
EMAIL_HOST_USER = get_env_value('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_value('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = get_env_value('EMAIL_USE_TLS', 'True').lower() in ('true', 't', 'yes', 'y', '1')
EMAIL_USE_SSL = get_env_value('EMAIL_USE_SSL', 'False').lower() in ('true', 't', 'yes', 'y', '1')
DEFAULT_FROM_EMAIL = get_env_value('DEFAULT_FROM_EMAIL')

# Cache settings (use Redis or Memcached in production)
REDIS_URL = get_env_value('REDIS_URL')
if REDIS_URL:
    try:
        CACHES = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': REDIS_URL,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'PARSER_CLASS': 'redis.connection.HiredisParser',
                    'SOCKET_CONNECT_TIMEOUT': int(get_env_value('REDIS_SOCKET_TIMEOUT', 5)),
                    'SOCKET_TIMEOUT': int(get_env_value('REDIS_SOCKET_TIMEOUT', 5)),
                }
            }
        }
        # Use Redis as session backend if configured
        if get_env_value('USE_REDIS_SESSIONS', 'False').lower() in ('true', 't', 'yes', 'y', '1'):
            SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
            SESSION_CACHE_ALIAS = 'default'
    except ImportError:
        raise ImportError(
            "The django-redis package is required when using REDIS_URL. "
            "Install it with: pip install django-redis"
        )

# API Keys should be stored in environment variables only
# Do not store API keys in settings files

# Configure logging for production
# Production-specific logging configuration that overrides base settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {module} {process:d} {thread:d} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'json': {
            'format': '{\'time\':\'{asctime}\', \'level\':\'{levelname}\', \'name\':\'{name}\', \'module\':\'{module}\', \'message\':\'{message}\'}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'production-errors.log'),
            'formatter': 'verbose',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
        },
        'file_warnings': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'production-warnings.log'),
            'formatter': 'verbose',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 14,
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'production-info.log'),
            'formatter': 'json',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        'file_security': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'production-security.log'),
            'formatter': 'verbose',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
        },
    },
    'loggers': {
        # Root logger
        '': {
            'handlers': ['console', 'file_errors', 'file_warnings'],
            'level': 'WARNING',
            'propagate': True,
        },
        # Django loggers
        'django': {
            'handlers': ['console', 'file_errors', 'file_warnings', 'file_info'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security.csrf': {
            'handlers': ['file_security', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        # Application loggers
        'inspireIA': {
            'handlers': ['console', 'file_errors', 'file_warnings', 'file_info'],
            'level': 'INFO',
            'propagate': False,
        },
        'catalog': {
            'handlers': ['file_errors', 'file_warnings', 'file_info'],
            'level': 'INFO',
            'propagate': False,
        },
        'users': {
            'handlers': ['file_errors', 'file_warnings', 'file_info'],
            'level': 'INFO',
            'propagate': False,
        },
        'interaction': {
            'handlers': ['file_errors', 'file_warnings', 'file_info'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            'handlers': ['file_errors', 'file_warnings', 'file_info'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['file_errors', 'file_warnings', 'file_info'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
AUTH_USER_MODEL = 'users.CustomUser'

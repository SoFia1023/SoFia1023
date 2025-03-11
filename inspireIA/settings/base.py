"""
Base settings for inspireIA project.
Contains settings common to all environments.
"""
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Note: BASE_DIR is also defined in __init__.py for dotenv loading
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Helper function to get environment variables with defaults
def get_env_value(env_variable: str, default_value: Any = None) -> Any:
    """
    Get an environment variable or return a default value
    """
    return os.environ.get(env_variable, default_value)

# Application definition
INSTALLED_APPS: List[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
    'users',
    'interaction',
]

MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'inspireIA.middleware.RequestLogMiddleware',
]

ROOT_URLCONF: str = 'inspireIA.urls'

TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'inspireIA' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'catalog.context_processors.ai_categories',
            ],
        },
    },
]

WSGI_APPLICATION: str = 'inspireIA.wsgi.application'

# Database
# Default to SQLite, but can be overridden in environment-specific settings
DATABASES: Dict[str, Dict[str, Any]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': int(get_env_value('MIN_PASSWORD_LENGTH', 8)),
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE: str = get_env_value('LANGUAGE_CODE', 'en-us')
TIME_ZONE: str = get_env_value('TIME_ZONE', 'UTC')
USE_I18N: bool = True
USE_TZ: bool = True

# Default primary key field type
DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
STATIC_URL: str = get_env_value('STATIC_URL', 'static/')
STATIC_ROOT: Path = BASE_DIR / 'staticfiles'
STATICFILES_DIRS: List[Path] = [BASE_DIR / 'static']

# Media files
MEDIA_URL: str = get_env_value('MEDIA_URL', '/media/')
MEDIA_ROOT: Path = BASE_DIR / 'media'

# Custom user model
AUTH_USER_MODEL: str = 'users.CustomUser'

# Authentication settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'requests.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'inspireIA.request': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

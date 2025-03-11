# Settings Module Documentation

This document explains the settings structure and environment variable usage in the Inspire AI project.

## Table of Contents

1. [Overview](#overview)
2. [Settings Structure](#settings-structure)
3. [Environment Variables](#environment-variables)
4. [Environment Selection](#environment-selection)
5. [Local Development](#local-development)
6. [Testing](#testing)
7. [Production Deployment](#production-deployment)
8. [Adding New Settings](#adding-new-settings)

## Overview

The Inspire AI project uses a modular settings approach with environment-specific configuration files and environment variables for sensitive or deployment-specific settings. This approach follows Django best practices and allows for flexible configuration across different environments.

## Settings Structure

The settings are organized into the following files:

```
inspireIA/
└── settings/
    ├── __init__.py       # Environment selection logic
    ├── base.py           # Common settings shared across all environments
    ├── development.py    # Development-specific settings
    ├── testing.py        # Testing-specific settings
    ├── production.py     # Production-specific settings
    ├── local.py          # Local overrides (gitignored)
    └── local.py.example  # Template for local.py
```

### File Purposes

- **`__init__.py`**: Handles environment selection logic and loads environment variables from `.env` file
- **`base.py`**: Contains settings common to all environments (installed apps, middleware, etc.)
- **`development.py`**: Development-specific settings (debug mode, console email backend, etc.)
- **`testing.py`**: Testing-specific settings (in-memory database, faster password hasher, etc.)
- **`production.py`**: Production-specific settings (security, caching, etc.)
- **`local.py`**: Optional local overrides for development (not version controlled)

## Environment Variables

The project uses [python-dotenv](https://github.com/theskumar/python-dotenv) to load environment variables from a `.env` file. This file should be created in the project root directory based on the `.env.example` template.

### Key Environment Variables

| Variable | Description | Default | Used In |
|----------|-------------|---------|---------|
| `DJANGO_ENV` | Environment to use (development, testing, production) | `development` | `__init__.py` |
| `DJANGO_SECRET_KEY` | Django secret key | Development key (in dev) | All |
| `DEBUG` | Debug mode | `True` in development, `False` in production | All |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` in development | All |
| `DATABASE_URL` | Database connection URL | SQLite (if not set) | All |
| `USE_S3` | Whether to use S3 for static/media files | `False` | Production |
| `REDIS_URL` | Redis connection URL for caching | None | Production |
| `OPENAI_API_KEY` | OpenAI API key | None | All |
| `HUGGINGFACE_API_KEY` | HuggingFace API key | None | All |

See the `.env.example` file for a complete list of available environment variables.

## Environment Selection

The environment is selected based on the `DJANGO_ENV` environment variable:

```python
# In __init__.py
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development').lower()

if DJANGO_ENV == 'production':
    from .production import *
elif DJANGO_ENV == 'testing':
    from .testing import *
else:
    from .development import *
```

You can set the environment in your `.env` file or directly in your shell:

```bash
# In .env file
DJANGO_ENV=production

# Or in shell
export DJANGO_ENV=production
```

## Local Development

For local development:

1. Copy `.env.example` to `.env` and customize as needed:
   ```bash
   cp .env.example .env
   ```

2. Optionally create a `local.py` file for settings that should not be committed:
   ```bash
   cp inspireIA/settings/local.py.example inspireIA/settings/local.py
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Using the Debug Toolbar

To enable the Django Debug Toolbar in development:

1. Set `ENABLE_DEBUG_TOOLBAR=True` in your `.env` file
2. Make sure `django-debug-toolbar` is installed:
   ```bash
   pip install django-debug-toolbar
   ```

## Testing

For testing:

1. Set `DJANGO_ENV=testing` in your environment or `.env` file
2. Run tests:
   ```bash
   pytest
   ```

The testing environment uses:
- In-memory SQLite database for faster tests
- Simplified password hashing
- Disabled migrations
- Console email backend
- Reduced logging

## Production Deployment

For production deployment:

1. Set `DJANGO_ENV=production`
2. Set all required environment variables (see `.env.example`)
3. Ensure `DEBUG=False`
4. Set `ALLOWED_HOSTS` to your domain(s)
5. Set a strong `DJANGO_SECRET_KEY`
6. Configure database, cache, and storage settings

### Required Production Settings

The following environment variables are required in production:

- `DJANGO_SECRET_KEY`
- `ALLOWED_HOSTS`

### Database Configuration

In production, it's recommended to use PostgreSQL:

```
DATABASE_URL=postgres://user:password@host:port/dbname
```

### Static and Media Files

For production, you can use S3 for static and media files:

```
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

### Caching

For production, it's recommended to use Redis for caching:

```
REDIS_URL=redis://host:port/db
USE_REDIS_SESSIONS=True
```

## Adding New Settings

When adding new settings:

1. Add the setting to the appropriate settings file (usually `base.py` for common settings)
2. Use the `get_env_value()` helper function for environment variable-based settings
3. Add type hints for better code quality
4. Add the environment variable to `.env.example` with documentation
5. Update this documentation if necessary

### Example

```python
# In base.py
MY_SETTING: str = get_env_value('MY_SETTING', 'default_value')
```

```
# In .env.example
MY_SETTING=default_value  # Description of what this setting does
```

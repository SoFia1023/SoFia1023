"""
Django settings module for inspireIA project.

This module handles environment selection logic and loads appropriate settings.
It uses python-dotenv to load environment variables from .env file.
"""
import os
import sys
from pathlib import Path

# Import python-dotenv for environment variable management
try:
    from dotenv import load_dotenv
except ImportError:
    # Output a helpful error message if python-dotenv is not installed
    print("Error: python-dotenv package is required. Install it with 'pip install python-dotenv'.")
    sys.exit(1)

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env file if it exists
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Determine which settings module to use based on DJANGO_ENV
# Default to 'development' if not specified
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development').lower()

# Import appropriate settings module
if DJANGO_ENV == 'production':
    from .production import *
elif DJANGO_ENV == 'testing':
    from .testing import *
else:
    from .development import *

# Override settings with local settings if available
try:
    from .local import *
except ImportError:
    # Local settings are optional
    pass

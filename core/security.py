"""
Security utilities for handling sensitive data like API keys.

This module provides functions for securely handling API keys and other sensitive data.
It implements encryption for sensitive values and secure retrieval methods.
"""
import base64
import logging
import os
from typing import Any, Dict, Optional, Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


def get_encryption_key() -> bytes:
    """
    Get or generate the encryption key for sensitive data.
    
    The key is derived from ENCRYPTION_KEY_SALT and SECRET_KEY.
    """
    # Get the salt from environment or settings
    salt = getattr(settings, "ENCRYPTION_KEY_SALT", None)
    if not salt:
        salt = os.environ.get("ENCRYPTION_KEY_SALT")
    
    if not salt:
        raise ImproperlyConfigured(
            "ENCRYPTION_KEY_SALT must be set in environment variables or settings"
        )
    
    # Use Django's SECRET_KEY as the password
    password = settings.SECRET_KEY.encode()
    salt = salt.encode()
    
    # Generate a key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt_value(value: str) -> str:
    """
    Encrypt a sensitive value using Fernet symmetric encryption.
    
    Args:
        value: The plaintext value to encrypt
        
    Returns:
        The encrypted value as a base64-encoded string
    """
    if not value:
        return ""
    
    try:
        key = get_encryption_key()
        f = Fernet(key)
        encrypted_data = f.encrypt(value.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    except Exception as e:
        logger.error(f"Error encrypting value: {str(e)}")
        # Return empty string on error rather than exposing the original value
        return ""


def decrypt_value(encrypted_value: str) -> str:
    """
    Decrypt a value that was encrypted with encrypt_value.
    
    Args:
        encrypted_value: The encrypted value as a base64-encoded string
        
    Returns:
        The decrypted plaintext value
    """
    if not encrypted_value:
        return ""
    
    try:
        key = get_encryption_key()
        f = Fernet(key)
        decrypted_data = f.decrypt(base64.urlsafe_b64decode(encrypted_value))
        return decrypted_data.decode()
    except Exception as e:
        logger.error(f"Error decrypting value: {str(e)}")
        return ""


def get_api_key(key_name: str) -> str:
    """
    Securely retrieve an API key from environment variables.
    
    Args:
        key_name: The name of the API key (e.g., 'OPENAI_API_KEY')
        
    Returns:
        The API key value or empty string if not found
    """
    # Always prioritize environment variables for API keys
    api_key = os.environ.get(key_name, "")
    
    # If not found in environment, check settings as fallback (not recommended for production)
    if not api_key and hasattr(settings, key_name):
        api_key = getattr(settings, key_name, "")
        if api_key:
            logger.warning(
                f"{key_name} found in settings but not in environment variables. "
                "This is not recommended for production environments."
            )
    
    return api_key

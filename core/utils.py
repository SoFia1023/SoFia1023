"""
Core utility functions shared across the entire project.

This module contains utility functions that are used by multiple apps
throughout the project.
"""
from typing import Any, Dict, List, Optional, TypeVar, Union, cast
import os
import json
from django.conf import settings
from django.http import HttpRequest
from django.utils.text import slugify


def get_client_ip(request: HttpRequest) -> str:
    """
    Get the client IP address from the request.
    
    Args:
        request: The HTTP request object
        
    Returns:
        The client's IP address as a string
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """
    Safely load JSON string, returning default value on error.
    
    Args:
        json_str: JSON string to parse
        default: Default value to return if parsing fails
        
    Returns:
        Parsed JSON data or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def create_unique_slug(model_instance: Any, slugable_field_name: str, 
                      slug_field_name: str = 'slug') -> str:
    """
    Create a unique slug for a model instance.
    
    Args:
        model_instance: The model instance to create a slug for
        slugable_field_name: The name of the field to base the slug on
        slug_field_name: The name of the slug field
        
    Returns:
        A unique slug string
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    model_class = model_instance.__class__
    extension = 1
    
    # Check if the slug already exists and make it unique if needed
    while model_class.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{extension}"
        extension += 1
        
    return unique_slug


def format_file_size(size_in_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_in_bytes: File size in bytes
        
    Returns:
        Human-readable file size string
    """
    # Convert bytes to appropriate unit
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024 or unit == 'TB':
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024


def is_valid_image_extension(filename: str) -> bool:
    """
    Check if a filename has a valid image extension.
    
    Args:
        filename: The filename to check
        
    Returns:
        True if the file has a valid image extension, False otherwise
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    _, extension = os.path.splitext(filename.lower())
    return extension in valid_extensions


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to a maximum length, adding a suffix if truncated.
    
    Args:
        text: The text to truncate
        max_length: Maximum length of the truncated text
        suffix: Suffix to add if the text is truncated
        
    Returns:
        Truncated text with suffix if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

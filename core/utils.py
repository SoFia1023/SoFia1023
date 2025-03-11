"""
Core utility functions shared across the entire project.

This module contains utility functions that are used by multiple apps
throughout the project.
"""
from typing import Any, Dict, List, Optional, TypeVar, Union, cast, Tuple
import os
import json
import csv
from io import StringIO
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


def format_conversation_for_download(conversation: Any, format_type: str = 'json') -> Tuple[str, str, str]:
    """
    Format a conversation for download in the specified format.
    
    This function converts a conversation and its messages into one of several downloadable formats.
    Supported formats include JSON, plain text, and CSV.
    
    Args:
        conversation: The Conversation object to format with its associated messages
        format_type: The format type to convert to ('json', 'txt', or 'csv')
        
    Returns:
        Tuple[str, str, str]: A tuple containing:
            - formatted_content: The conversation content in the requested format
            - content_type: The MIME type for the content (e.g., 'application/json')
            - file_extension: The appropriate file extension (e.g., 'json')
            
    Raises:
        ValueError: If an invalid format_type is provided
    """
    messages = conversation.get_messages()
    
    if format_type == 'json':
        # Use the built-in to_json method
        content = conversation.to_json()
        content_type = 'application/json'
        file_ext = 'json'
        
    elif format_type == 'txt':
        # Simple text format
        lines = [f"Conversation: {conversation.title}"]
        lines.append(f"AI Tool: {conversation.ai_tool.name if conversation.ai_tool else 'Unknown'}")
        lines.append(f"Date: {conversation.created_at.strftime('%Y-%m-%d %H:%M')}")
        lines.append("-" * 40)
        
        for msg in messages:
            sender = "You" if msg.is_user else (conversation.ai_tool.name if conversation.ai_tool else "AI")
            timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M')
            lines.append(f"{sender} ({timestamp}):")
            lines.append(msg.content)
            lines.append("")
            
        content = "\n".join(lines)
        content_type = 'text/plain'
        file_ext = 'txt'
        
    elif format_type == 'csv':
        # CSV format
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Timestamp', 'Sender', 'Message'])
        
        for msg in messages:
            sender = "User" if msg.is_user else (conversation.ai_tool.name if conversation.ai_tool else "AI")
            writer.writerow([
                msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                sender,
                msg.content
            ])
            
        content = output.getvalue()
        content_type = 'text/csv'
        file_ext = 'csv'
        
    else:
        # Default to JSON if format not recognized
        content = conversation.to_json()
        content_type = 'application/json'
        file_ext = 'json'
        
    return content, content_type, file_ext

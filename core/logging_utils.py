"""
Logging utilities for the InspireIA application.

This module provides helper functions and classes for consistent logging
across the application.
"""
import logging
from typing import Any, Dict, Optional, Union


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: The name of the logger, typically the module name (__name__)
        
    Returns:
        A configured logger instance
    """
    return logging.getLogger(name)


class LoggingMixin:
    """
    A mixin that provides logging capabilities to a class.
    
    This mixin automatically creates a logger for the class using the class's
    module and name.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the mixin with a logger."""
        self.logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")
        super().__init__(*args, **kwargs)


def log_exception(
    logger: logging.Logger, 
    exc: Exception, 
    message: str = "An exception occurred", 
    extra: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log an exception with additional context.
    
    Args:
        logger: The logger to use
        exc: The exception to log
        message: A message describing the context of the exception
        extra: Additional data to include in the log
    """
    if extra is None:
        extra = {}
    
    # Add exception details to the extra dict
    exc_info = {
        'exception_type': type(exc).__name__,
        'exception_message': str(exc),
    }
    
    # Merge the exception info with any provided extra info
    log_extra = {**extra, **exc_info}
    
    # Log the exception with the merged extra data
    logger.exception(message, extra=log_extra)


def log_api_request(
    logger: logging.Logger,
    service_name: str,
    endpoint: str,
    method: str,
    status_code: Optional[int] = None,
    response_time: Optional[float] = None,
    request_data: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None
) -> None:
    """
    Log an API request with relevant details.
    
    Args:
        logger: The logger to use
        service_name: Name of the external service (e.g., 'OpenAI', 'HuggingFace')
        endpoint: The API endpoint called
        method: HTTP method used (GET, POST, etc.)
        status_code: HTTP status code of the response
        response_time: Time taken for the request in seconds
        request_data: Dictionary containing request data (sensitive data should be redacted)
        error: Error message if the request failed
    """
    log_data = {
        'service': service_name,
        'endpoint': endpoint,
        'method': method,
    }
    
    if status_code is not None:
        log_data['status_code'] = status_code
    
    if response_time is not None:
        log_data['response_time'] = f"{response_time:.3f}s"
    
    if request_data is not None:
        # Ensure we don't log sensitive data
        safe_data = _redact_sensitive_data(request_data)
        log_data['request_data'] = safe_data
    
    if error:
        log_data['error'] = error
        logger.error(f"API request to {service_name} failed", extra=log_data)
    else:
        logger.info(f"API request to {service_name} completed", extra=log_data)


def _redact_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Redact sensitive data from a dictionary.
    
    Args:
        data: Dictionary that may contain sensitive data
        
    Returns:
        Dictionary with sensitive data redacted
    """
    sensitive_keys = [
        'api_key', 'key', 'secret', 'password', 'token', 'auth', 
        'authorization', 'access_token', 'refresh_token'
    ]
    
    result = {}
    for key, value in data.items():
        # Check if this key or any part of it matches sensitive keys
        is_sensitive = any(sensitive in key.lower() for sensitive in sensitive_keys)
        
        if is_sensitive:
            result[key] = '********'
        elif isinstance(value, dict):
            # Recursively redact nested dictionaries
            result[key] = _redact_sensitive_data(value)
        else:
            result[key] = value
            
    return result


def log_user_activity(
    logger: logging.Logger,
    user_id: Union[int, str],
    action: str,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None
) -> None:
    """
    Log user activity for audit purposes.
    
    Args:
        logger: The logger to use
        user_id: User identifier
        action: Description of the action performed
        details: Additional details about the action
        ip_address: IP address of the user
    """
    log_data = {
        'user_id': user_id,
        'action': action,
    }
    
    if details:
        log_data['details'] = details
        
    if ip_address:
        log_data['ip_address'] = ip_address
    
    logger.info(f"User {user_id} performed {action}", extra=log_data)

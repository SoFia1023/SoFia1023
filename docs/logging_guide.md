# InspireIA Logging Guide

This guide provides a comprehensive overview of the logging system implemented in the InspireIA application, with practical examples and best practices.

## Table of Contents

1. [Introduction](#introduction)
2. [Logging Architecture](#logging-architecture)
3. [Logging Components](#logging-components)
   - [Middleware Logging](#middleware-logging)
   - [Form Logging](#form-logging)
   - [API Logging](#api-logging)
   - [Exception Logging](#exception-logging)
   - [User Activity Logging](#user-activity-logging)
4. [Using the Logging System](#using-the-logging-system)
5. [Testing the Logging System](#testing-the-logging-system)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Introduction

The InspireIA application uses a structured logging system to capture important events, errors, and user activities. This helps with debugging, monitoring, and auditing the application.

## Logging Architecture

The logging system is built on top of Python's standard logging module and Django's logging framework, with enhancements for structured logging and context preservation.

Key components:
- **Formatters**: Define how log messages are formatted
- **Handlers**: Determine where logs are sent (console, files, external services)
- **Loggers**: Named entities that route log messages to appropriate handlers
- **Middleware**: Captures HTTP request/response information
- **Utility Functions**: Simplify common logging patterns

## Logging Components

### Middleware Logging

The `RequestLogMiddleware` automatically logs information about each HTTP request, including:
- Request path, method, and status code
- Processing time
- User information
- IP address and user agent
- Query parameters (with sensitive data redacted)

### Form Logging

Enhanced logging for user forms, particularly in authentication and profile management:
- Authentication attempts (successful and failed)
- Specific reasons for authentication failures
- Profile updates with details of changed fields
- Form validation errors with context
- User registration events

Example:
```python
# In a form validation method
def clean_email(self) -> str:
    email = self.cleaned_data.get('email')
    
    if email and User.objects.filter(email=email).exists():
        logger.warning(
            f"Registration attempt with duplicate email: {email}",
            extra={
                'email': email,
                'action': 'registration_failed',
                'reason': 'duplicate_email'
            }
        )
        raise forms.ValidationError('Email is already in use')
        
    return email
```

### API Logging

Structured logging for API requests to external services:
- Service name and endpoint
- Request method and data
- Response status code and time
- Error information for failed requests

Example:
```python
from core.logging_utils import log_api_request

# Log a successful API request
log_api_request(
    logger=logger,
    service_name="OpenAI",
    endpoint="/v1/completions",
    method="POST",
    status_code=200,
    response_time=1.25,
    request_data={"prompt": "Hello, world", "max_tokens": 50},
)
```

### Exception Logging

Detailed logging of exceptions with context:
- Exception type and message
- Stack trace
- Additional context about the operation
- User information (if available)

Example:
```python
from core.logging_utils import log_exception

try:
    # Some operation that might fail
    result = process_data(data)
except Exception as e:
    log_exception(
        logger=logger,
        exc=e,
        message="Failed to process data",
        extra={"data_id": data.id, "operation": "process_data"}
    )
```

### User Activity Logging

Tracking user actions throughout the application:
- Login and logout events
- Resource creation and modification
- Important user interactions
- Security-related events

Example:
```python
from core.logging_utils import log_user_activity

# Log a user action
log_user_activity(
    logger=logger,
    user_id=request.user.id,
    action="create_prompt",
    details={"prompt_id": prompt.id, "title": prompt.title},
    ip_address=get_client_ip(request),
)
```

## Using the Logging System

To use the logging system in your code:

1. Get a logger for your module:
```python
from core.logging_utils import get_logger
logger = get_logger(__name__)
```

2. Log messages with appropriate levels:
```python
# Debug information (development only)
logger.debug("Processing item %s", item_id)

# Informational messages
logger.info("User %s created a new prompt", user.username)

# Warning conditions
logger.warning("Rate limit approaching for user %s", user.username)

# Error conditions
logger.error("Failed to process payment for order %s", order_id)

# Critical conditions
logger.critical("Database connection lost")
```

3. Add structured context with the `extra` parameter:
```python
logger.info(
    "Prompt created successfully",
    extra={
        "prompt_id": prompt.id,
        "user_id": user.id,
        "category": prompt.category,
        "is_public": prompt.is_public
    }
)
```

## Testing the Logging System

The application includes a management command to test the logging system:

```bash
# Test all logging features
python manage.py test_logging --all

# Test specific log levels
python manage.py test_logging --level=debug
python manage.py test_logging --level=info
python manage.py test_logging --level=warning
python manage.py test_logging --level=error
python manage.py test_logging --level=critical

# Test specific logging components
python manage.py test_logging --forms
```

## Best Practices

1. **Use the appropriate log level**:
   - DEBUG: Detailed diagnostic information
   - INFO: General operational information
   - WARNING: Unexpected events that don't affect normal operation
   - ERROR: Errors that prevent a function from working
   - CRITICAL: Critical errors that require immediate attention

2. **Include context in log messages**:
   - Use the `extra` parameter to add structured context
   - Include relevant IDs (user_id, object_id, etc.)
   - Add action names for easier filtering

3. **Don't log sensitive information**:
   - Passwords, tokens, or API keys
   - Personal identifiable information (PII)
   - Financial information

4. **Be consistent with log formats**:
   - Use the utility functions provided by `core.logging_utils`
   - Follow established patterns for similar events
   - Use descriptive action names

5. **Log at service boundaries**:
   - API calls to external services
   - Database operations
   - File system interactions

## Troubleshooting

If logs are not appearing as expected:

1. Check the log level configuration in settings
2. Verify that the appropriate handlers are configured
3. Ensure the logs directory exists and is writable
4. Check that the logger name matches the configuration

For more detailed information, refer to the [full logging documentation](logging.md).

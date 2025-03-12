# Logging System Documentation

This document outlines the enhanced logging system implemented in the InspireIA application.

## Overview

The logging system is designed to provide comprehensive monitoring and debugging capabilities across different environments (development, testing, production). It follows Django best practices and provides a consistent approach to logging throughout the application.

## Key Features

- **Environment-specific configurations**: Different logging setups for development, testing, and production
- **Rotating log files**: Prevents log files from growing too large
- **Colored console output**: Makes development logs easier to read
- **JSON formatting**: For production logs to facilitate log aggregation and analysis
- **Email notifications**: Critical errors are sent to administrators in production
- **Security logging**: Dedicated security log for tracking security-related events
- **Performance monitoring**: Tracks API request performance
- **User activity tracking**: For audit and security purposes

## Log Files

The application creates several log files in the `logs/` directory:

### Base Configuration (All Environments)
- `general.log`: General application logs (INFO and above)
- `errors.log`: Error logs (ERROR and above)
- `security.log`: Security-related logs
- `requests.log`: HTTP request logs
- `db.log`: Database query logs (WARNING and above)

### Development Environment
- `debug.log`: Detailed debug logs (DEBUG and above)

### Production Environment
- `production-errors.log`: Error logs with daily rotation
- `production-warnings.log`: Warning logs with daily rotation
- `production-info.log`: Info logs in JSON format with daily rotation
- `production-security.log`: Security logs with daily rotation

## Log Levels

The logging system uses standard Python logging levels:

- **DEBUG**: Detailed information, typically of interest only when diagnosing problems
- **INFO**: Confirmation that things are working as expected
- **WARNING**: An indication that something unexpected happened, or may happen in the near future
- **ERROR**: Due to a more serious problem, the software has not been able to perform some function
- **CRITICAL**: A serious error, indicating that the program itself may be unable to continue running

## Using the Logging System

### Basic Usage

```python
import logging

# Get a logger for the current module
logger = logging.getLogger(__name__)

# Log at different levels
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

### Using the Logging Utilities

The application provides a `core.logging_utils` module with helper functions and classes:

```python
from core.logging_utils import get_logger, log_exception, log_api_request, log_user_activity

# Get a logger for the current module
logger = get_logger(__name__)

# Log an exception with context
try:
    # Some code that might raise an exception
    result = 1 / 0
except Exception as e:
    log_exception(logger, e, "Division operation failed", {"value": 0})

# Log an API request
log_api_request(
    logger=logger,
    service_name="OpenAI",
    endpoint="/v1/chat/completions",
    method="POST",
    status_code=200,
    response_time=1.25,
    request_data={"model": "gpt-4", "messages": [{"role": "user", "content": "Hello"}]},
)

# Log user activity
log_user_activity(
    logger=logger,
    user_id=123,
    action="login",
    ip_address="192.168.1.1"
)
```

### Using the LoggingMixin

For class-based views or other classes that need logging:

```python
from core.logging_utils import LoggingMixin
from django.views import View

class MyView(LoggingMixin, View):
    def get(self, request, *args, **kwargs):
        self.logger.info("Processing GET request")
        # View logic here
        return response
```

## Configuration Details

### Base Configuration

The base configuration in `inspireIA/settings/base.py` sets up the foundation of the logging system with handlers for different log types and loggers for different parts of the application.

### Development Configuration

The development configuration in `inspireIA/settings/development.py` enhances the base configuration with:

- Colored console output using the `colorlog` package
- More verbose logging (DEBUG level for application loggers)
- SQL query logging for debugging database issues

### Production Configuration

The production configuration in `inspireIA/settings/production.py` focuses on:

- Rotating log files with daily rotation
- JSON formatting for easier log aggregation
- Email notifications for critical errors
- Reduced console output (WARNING level and above)
- Separate log files for different severity levels

## Best Practices

1. **Use the appropriate log level**: 
   - DEBUG for detailed diagnostic information
   - INFO for general operational information
   - WARNING for unexpected events that don't affect normal operation
   - ERROR for errors that prevent a function from working
   - CRITICAL for errors that might cause the application to crash

2. **Include context in log messages**:
   - Use the `extra` parameter to include additional context
   - Structure log messages to be easily parseable
   - Include relevant IDs (user ID, request ID, etc.)

3. **Don't log sensitive information**:
   - Never log passwords, API keys, or other sensitive data
   - Use the `_redact_sensitive_data` function in `logging_utils.py` when logging request data

4. **Use structured logging in production**:
   - JSON format makes logs easier to parse and analyze
   - Include relevant metadata with each log entry

5. **Log exceptions properly**:
   - Use `logger.exception()` or the `log_exception()` utility to include the traceback
   - Include context about what led to the exception

## Monitoring and Analysis

For production environments, consider setting up a log aggregation and analysis system like:

- ELK Stack (Elasticsearch, Logstash, Kibana)
- Graylog
- Datadog
- New Relic
- Sentry (especially for error tracking)

These tools can help you:
- Centralize logs from multiple servers
- Set up alerts for critical issues
- Visualize trends and patterns
- Quickly search and filter logs

## Form Logging

The application includes enhanced logging for user forms, particularly in authentication and profile management. This is implemented in `users/forms.py` and provides structured logging of form validation, submission, and errors.

### Features

- Logs authentication attempts (successful and failed)
- Records specific reasons for authentication failures
- Tracks profile updates with details of changed fields
- Logs form validation errors with context
- Captures user registration events

### Example Log Output

```json
{
  "timestamp": "2025-03-11T20:42:15.123456",
  "level": "INFO",
  "message": "User john_doe updated profile fields: email, first_name, bio",
  "username": "john_doe",
  "user_id": 42,
  "updated_fields": ["email", "first_name", "bio"],
  "action": "profile_update"
}
```

### Implementation

To add structured logging to your own forms:

1. Get a logger for your module:

```python
from core.logging_utils import get_logger
logger = get_logger(__name__)
```

2. Add logging to form validation methods:

```python
def clean_email(self) -> str:
    email = self.cleaned_data.get('email')
    
    if email and User.objects.filter(email=email).exists():
        # Log validation error
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

3. Add logging to form save methods:

```python
def save(self, commit: bool = True) -> Any:
    user = super().save(commit=False)
    
    if commit:
        user.save()
        
        # Log successful action
        logger.info(
            f"User {user.username} action completed",
            extra={
                'user_id': user.id,
                'username': user.username,
                'action': 'user_action'
            }
        )
    
    return user
```

## Middleware Logging

The application includes a `RequestLogMiddleware` that logs detailed information about each HTTP request. This middleware is configured in `inspireIA/middleware.py` and provides structured logging of request data.

### Features

- Logs request path, method, and status code
- Records request processing time
- Includes user information when authenticated
- Captures IP address and user agent
- Logs query parameters (with sensitive data redacted)
- Provides additional context for error responses

### Example Log Output

```json
{
  "timestamp": "2025-03-11T20:35:34.123456",
  "method": "GET",
  "path": "/catalog/prompts/",
  "status_code": 200,
  "duration": "0.125s",
  "ip_address": "192.168.1.1",
  "user": {
    "id": 42,
    "username": "john_doe",
    "is_staff": false
  },
  "headers": {
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "referer": "https://example.com/previous-page/"
  },
  "query_params": {
    "page": "2",
    "sort": "date"
  }
}
```

## API Request Logging

The application includes utilities for logging API requests to external services in a structured and consistent manner. This is implemented in the `catalog/api_utils.py` module.

### Features

- Logs request details (service, endpoint, method)
- Records response status code and time
- Redacts sensitive information from request data
- Provides detailed context for API errors
- Captures exceptions with full context

### Example Usage

```python
from core.logging_utils import get_logger, log_api_request

logger = get_logger(__name__)

def call_external_api(data):
    start_time = time.time()
    try:
        response = requests.post('https://api.example.com/endpoint', json=data)
        status_code = response.status_code
        response_time = time.time() - start_time
        
        log_api_request(
            logger=logger,
            service_name="ExampleAPI",
            endpoint="/endpoint",
            method="POST",
            status_code=status_code,
            response_time=response_time,
            request_data=data
        )
        
        return response.json()
    except Exception as e:
        log_exception(
            logger=logger,
            exc=e,
            message="API request failed",
            extra={
                'service': 'ExampleAPI',
                'endpoint': '/endpoint',
                'data': data
            }
        )
        raise
```

## Testing the Logging System

The application includes a management command to test the logging system. This command allows you to generate test log messages at different levels and verify that the logging configuration is working correctly.

### Usage

```bash
# Basic usage - generate info level logs
python manage.py test_logging

# Generate debug level logs
python manage.py test_logging --level=debug

# Generate multiple log messages
python manage.py test_logging --count=5

# Test all logging features
python manage.py test_logging --all

# Use a specific logger name/module
python manage.py test_logging --module=myapp.component
```

## Extending the Logging System

To add a new logger for a specific component:

1. Add the logger configuration to the LOGGING dictionary in the appropriate settings file:

```python
'loggers': {
    'my_component': {
        'handlers': ['console', 'file_general'],
        'level': 'INFO',
        'propagate': False,
    },
}
```

2. Use the logger in your code:

```python
import logging
logger = logging.getLogger('my_component')
logger.info("Component initialized")
```

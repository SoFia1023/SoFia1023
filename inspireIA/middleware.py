import time
import logging
from typing import Any, Callable, Dict, Optional

from django.http import HttpRequest, HttpResponse
from django.utils import timezone

class RequestLogMiddleware:
    """
    Middleware to log request details including timing information.
    
    This middleware logs:
    - Request path and method
    - User information (if authenticated)
    - Response status code
    - Request processing time
    - IP address
    - User agent
    - Referrer
    - Query parameters (excluding sensitive data)
    """
    
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        # Get a logger instance
        self.logger = logging.getLogger('inspireIA.request')
        
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Record start time
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        
        # Prepare log data
        log_data = self._prepare_log_data(request, response, duration)
        
        # Log the request with structured data
        self.logger.info(
            f"{request.method} {request.path} - Status: {response.status_code}",
            extra=log_data
        )
        
        return response
    
    def _prepare_log_data(self, request: HttpRequest, response: HttpResponse, duration: float) -> Dict[str, Any]:
        """
        Prepare structured log data from the request and response.
        
        Args:
            request: The HTTP request object
            response: The HTTP response object
            duration: Request processing time in seconds
            
        Returns:
            Dictionary with structured log data
        """
        # Basic request info
        log_data = {
            'timestamp': timezone.now().isoformat(),
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration': f"{duration:.3f}s",
            'ip_address': self._get_client_ip(request),
        }
        
        # Add user info if authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            log_data['user'] = {
                'id': request.user.id,
                'username': request.user.username,
                'is_staff': request.user.is_staff,
            }
        else:
            log_data['user'] = 'Anonymous'
        
        # Add HTTP headers info (selective)
        headers = {}
        if 'HTTP_USER_AGENT' in request.META:
            headers['user_agent'] = request.META['HTTP_USER_AGENT']
        if 'HTTP_REFERER' in request.META:
            headers['referer'] = request.META['HTTP_REFERER']
        if headers:
            log_data['headers'] = headers
        
        # Add query parameters (excluding sensitive ones)
        if request.GET:
            # Filter out potentially sensitive parameters
            safe_params = self._filter_sensitive_params(request.GET.dict())
            if safe_params:
                log_data['query_params'] = safe_params
        
        # Add response info for non-success status codes
        if response.status_code >= 400:
            log_data['is_error'] = True
            # For 4xx errors, include more details
            if 400 <= response.status_code < 500:
                log_data['error_type'] = 'client_error'
            else:
                log_data['error_type'] = 'server_error'
        
        return log_data
    
    def _get_client_ip(self, request: HttpRequest) -> str:
        """
        Get the client IP address from the request.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Client IP address as string
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # X-Forwarded-For can be a comma-separated list of IPs.
            # The client's IP will be the first one.
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip
    
    def _filter_sensitive_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter out sensitive parameters from query parameters.
        
        Args:
            params: Dictionary of query parameters
            
        Returns:
            Dictionary with sensitive parameters redacted
        """
        sensitive_keys = ['password', 'token', 'key', 'secret', 'auth', 'credentials']
        filtered_params = {}
        
        for key, value in params.items():
            # Check if this key contains any sensitive terms
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                filtered_params[key] = '********'
            else:
                filtered_params[key] = value
                
        return filtered_params
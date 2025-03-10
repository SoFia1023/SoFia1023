import time
import logging
from django.utils import timezone

# Get a logger instance
logger = logging.getLogger('inspireIA.request')

class RequestLogMiddleware:
    """
    Middleware to log request details including timing information.
    
    This middleware logs:
    - Request path
    - Request method
    - User (if authenticated)
    - Response status code
    - Request processing time
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Record start time
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate request duration
        duration = time.time() - start_time
        
        # Get user info if authenticated
        user_info = "Anonymous"
        if request.user.is_authenticated:
            user_info = f"{request.user.username} (ID: {request.user.id})"
        
        # Log the request
        logger.info(
            f"[{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{request.method} {request.path} - "
            f"User: {user_info} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.2f}s"
        )
        
        return response 
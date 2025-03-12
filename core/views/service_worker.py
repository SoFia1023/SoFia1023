"""
Service worker view module.

This module contains a view to serve the service-worker.js file from the root of the site.
"""
from django.http import HttpRequest, HttpResponse
import os
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from typing import Any


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # Cache for 24 hours
def service_worker(request: HttpRequest) -> HttpResponse:
    """
    View to serve the service-worker.js file from the root of the site.
    
    Args:
        request: The HTTP request object
        
    Returns:
        The service worker file with appropriate content type
    """
    # Path to the service worker file in the static directory
    service_worker_path = os.path.join(settings.STATIC_ROOT, 'service-worker.js')
    
    # If the file doesn't exist in STATIC_ROOT, try to find it in the static directory
    if not os.path.exists(service_worker_path):
        service_worker_path = os.path.join(settings.BASE_DIR, 'static', 'service-worker.js')
    
    # Read the file content
    with open(service_worker_path, 'r') as f:
        content = f.read()
    
    # Return the file with the correct content type
    return HttpResponse(content, content_type='application/javascript')

"""
API Logging Demo views.

This module contains views that demonstrate the API logging capabilities
of the InspireIA application.
"""
import json
import time
from typing import Any, Dict, Optional

import requests
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.logging_utils import get_logger, log_api_request, log_exception

# Get a logger for this module
logger = get_logger(__name__)


@require_http_methods(["GET", "POST"])
def api_logging_demo(request: HttpRequest) -> HttpResponse:
    """
    Demonstrate API logging capabilities.
    
    This view shows how to properly log API requests, including success and error cases.
    """
    context = {
        "title": "API Logging Demo",
        "description": "This demo shows how to log API requests with structured data",
    }
    
    if request.method == "POST":
        api_type = request.POST.get("api_type", "")
        
        if api_type == "success":
            # Simulate a successful API call
            log_successful_api_call()
            messages.success(
                request, 
                "Successful API call logged. Check the console and log files."
            )
            
        elif api_type == "error":
            # Simulate a failed API call
            log_failed_api_call()
            messages.warning(
                request, 
                "Failed API call logged. Check the console and log files."
            )
            
        elif api_type == "real":
            # Make a real API call to a public API
            result = make_real_api_call()
            if result["success"]:
                messages.success(
                    request, 
                    f"Real API call succeeded and was logged. Received {len(result.get('data', []))} items."
                )
            else:
                messages.error(
                    request, 
                    f"Real API call failed and was logged. Error: {result.get('error', 'Unknown error')}"
                )
                
        elif api_type == "exception":
            # Simulate an API call that raises an exception
            try:
                log_api_call_with_exception()
            except Exception as e:
                log_exception(
                    logger=logger,
                    exc=e,
                    message="Exception occurred during API call",
                    extra={"api_type": "exception_demo"}
                )
                messages.error(
                    request, 
                    "API call with exception logged. Check the console and log files."
                )
    
    return render(request, "core/api_logging_demo.html", context)


def log_successful_api_call() -> None:
    """Simulate and log a successful API call."""
    # Simulate API call duration
    time.sleep(0.5)
    
    # Log the successful API call
    log_api_request(
        logger=logger,
        service_name="ExampleAPI",
        endpoint="/api/v1/data",
        method="GET",
        status_code=200,
        response_time=0.5,
        request_data={
            "limit": 10,
            "offset": 0,
            "filter": "active",
            "api_key": "REDACTED"  # This will be automatically redacted
        }
    )
    
    logger.info(
        "Successfully retrieved data from ExampleAPI",
        extra={
            "service": "ExampleAPI",
            "items_count": 10,
            "cache_hit": False
        }
    )


def log_failed_api_call() -> None:
    """Simulate and log a failed API call."""
    # Simulate API call duration
    time.sleep(0.3)
    
    # Log the failed API call
    log_api_request(
        logger=logger,
        service_name="ExampleAPI",
        endpoint="/api/v1/restricted",
        method="POST",
        status_code=403,
        response_time=0.3,
        request_data={
            "user_id": 123,
            "action": "delete",
            "resource_id": 456,
            "auth_token": "REDACTED"  # This will be automatically redacted
        },
        error="Forbidden: Insufficient permissions to perform this action"
    )
    
    logger.error(
        "Failed to perform restricted action via ExampleAPI",
        extra={
            "service": "ExampleAPI",
            "user_id": 123,
            "resource_id": 456,
            "error_code": "INSUFFICIENT_PERMISSIONS"
        }
    )


def log_api_call_with_exception() -> None:
    """Simulate an API call that raises an exception."""
    # Simulate API call start
    start_time = time.time()
    
    # Simulate a connection error
    try:
        # This will raise a NameError
        undefined_variable = nonexistent_variable  # noqa
        
        # The following code won't be reached
        response_time = time.time() - start_time
        log_api_request(
            logger=logger,
            service_name="ExampleAPI",
            endpoint="/api/v1/data",
            method="GET",
            status_code=200,
            response_time=response_time,
            request_data={"query": "test"}
        )
    except Exception as e:
        # Calculate response time even though the request failed
        response_time = time.time() - start_time
        
        # Log the failed API request
        log_api_request(
            logger=logger,
            service_name="ExampleAPI",
            endpoint="/api/v1/data",
            method="GET",
            status_code=None,  # No status code since the request failed
            response_time=response_time,
            request_data={"query": "test"},
            error=f"Connection error: {str(e)}"
        )
        
        # Re-raise the exception to be caught by the caller
        raise


def make_real_api_call() -> Dict[str, Any]:
    """
    Make a real API call to a public API and log it.
    
    Returns:
        Dict with success status and data or error message
    """
    # Use JSONPlaceholder as a simple, reliable public API
    api_url = "https://jsonplaceholder.typicode.com/posts"
    
    start_time = time.time()
    result: Dict[str, Any] = {"success": False}
    
    try:
        # Make the actual API call
        response = requests.get(api_url, timeout=5)
        response_time = time.time() - start_time
        
        # Log the API request
        log_api_request(
            logger=logger,
            service_name="JSONPlaceholder",
            endpoint="/posts",
            method="GET",
            status_code=response.status_code,
            response_time=response_time,
            request_data={}
        )
        
        # Process the response
        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "data": data[:5],  # Only return the first 5 items
                "total": len(data)
            }
            
            logger.info(
                f"Successfully retrieved {len(data)} posts from JSONPlaceholder",
                extra={
                    "service": "JSONPlaceholder",
                    "items_count": len(data)
                }
            )
        else:
            error_msg = f"API returned status code {response.status_code}"
            result = {
                "success": False,
                "error": error_msg
            }
            
            logger.error(
                f"Failed to retrieve posts from JSONPlaceholder: {error_msg}",
                extra={
                    "service": "JSONPlaceholder",
                    "status_code": response.status_code
                }
            )
            
    except Exception as e:
        response_time = time.time() - start_time
        error_msg = str(e)
        
        # Log the failed API request
        log_api_request(
            logger=logger,
            service_name="JSONPlaceholder",
            endpoint="/posts",
            method="GET",
            status_code=None,
            response_time=response_time,
            request_data={},
            error=error_msg
        )
        
        log_exception(
            logger=logger,
            exc=e,
            message="Exception occurred during JSONPlaceholder API call",
            extra={"service": "JSONPlaceholder"}
        )
        
        result = {
            "success": False,
            "error": error_msg
        }
    
    return result


@require_http_methods(["GET"])
def api_logging_demo_json(request: HttpRequest) -> JsonResponse:
    """
    API endpoint that demonstrates JSON response logging.
    
    This view shows how to log API requests that return JSON responses.
    """
    start_time = time.time()
    
    # Simulate processing time
    time.sleep(0.2)
    
    # Prepare response data
    data = {
        "status": "success",
        "message": "API logging demo",
        "timestamp": time.time(),
        "data": {
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"},
                {"id": 3, "name": "Item 3"},
            ]
        }
    }
    
    # Log the API request
    response_time = time.time() - start_time
    log_api_request(
        logger=logger,
        service_name="InspireIA",
        endpoint="/api/logging-demo",
        method="GET",
        status_code=200,
        response_time=response_time,
        request_data=request.GET.dict()
    )
    
    logger.info(
        "API logging demo JSON endpoint called",
        extra={
            "response_time": response_time,
            "items_count": len(data["data"]["items"])
        }
    )
    
    return JsonResponse(data)

"""
URL configuration for the core app.
"""
from django.urls import path

from core.views.logging_demo import (
    logging_demo_basic,
    logging_demo_error,
    logging_demo_performance,
    logging_demo_class_view,
    logging_demo_user_forms,
)
from core.views.api_logging_demo import (
    api_logging_demo,
    api_logging_demo_json,
)

app_name = "core"

urlpatterns = [
    # Logging demo views
    path("demo/logging/", logging_demo_basic, name="logging_demo"),  # Main logging demo page
    path("demo/logging/basic/", logging_demo_basic, name="logging_demo_basic"),
    path("demo/logging/error/", logging_demo_error, name="logging_demo_error"),
    path("demo/logging/performance/", logging_demo_performance, name="logging_demo_performance"),
    path("demo/logging/class/", logging_demo_class_view, name="logging_demo_class"),
    path("demo/logging/forms/", logging_demo_user_forms, name="logging_demo_user_forms"),
    
    # API logging demo views
    path("demo/logging/api/", api_logging_demo, name="api_logging_demo"),
    path("demo/logging/api/json/", api_logging_demo_json, name="api_logging_demo_json"),
]

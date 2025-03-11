from django.apps import AppConfig
from typing import Any


class ApiConfig(AppConfig):
    """
    API app configuration.
    
    This app handles all API endpoints for the project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'API Endpoints'
    
    def ready(self) -> None:
        """
        Perform initialization tasks when the app is ready.
        """
        # Import signals or perform other initialization tasks
        pass

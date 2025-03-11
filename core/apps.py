from django.apps import AppConfig
from typing import Any


class CoreConfig(AppConfig):
    """Core app configuration.
    
    This app contains common functionality shared across the entire project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core Functionality'
    
    def ready(self) -> None:
        """Perform initialization tasks when the app is ready."""
        # Import signals or perform other initialization tasks
        pass

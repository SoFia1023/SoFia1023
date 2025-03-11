"""
Views package for the catalog app.

This package contains all views for the catalog app, organized into logical modules.
"""
# Import constants
from ..constants import CATEGORIES

# Import views for easy access
from .catalog import CatalogView, catalog_view, ModelsView, models_view
from .ai_tools import AIToolDetailView, presentationAI, compare_tools
from .auth import register_view, login_view, logout_view
from .profile import profile_view, toggle_favorite
from .home import home

"""
Views package for the users app.

This package contains all views for the users app, organized into logical modules.
"""
# Import views for easy access
from .auth import register, login_view, logout_view
from .profile import profile_view, update_profile, change_password
from .dashboard import dashboard

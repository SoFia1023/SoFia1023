""" urls.py in inspireIA project
URL configuration for inspireIA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from typing import List, Union, cast
from django.contrib import admin
from django.urls import path, include, URLPattern, URLResolver
from catalog.views.home import home
from django.conf import settings
from django.conf.urls.static import static
from .admin import admin_site

# Type hint for URL patterns
urlpatterns: List[Union[URLPattern, URLResolver]] = [
    # Admin sites
    path('admin/', admin.site.urls),  # Default admin site (for backward compatibility)
    path('inspire-admin/', admin_site.urls, name='inspire_admin'),  # Custom admin site
    
    # Home page
    path('', home, name='home'),
    
    # Catalog app - includes all catalog-related URLs
    path('catalog/', include('catalog.urls', namespace='catalog')),
    
    # Interaction app - handles chats, favorites, sharing
    path('interaction/', include('interaction.urls', namespace='interaction')),
    
    # Users app
    path('users/', include('users.urls')),
    
    # API app
    path('api/', include('api.urls')),
    

]

# Serve media files in development
if settings.DEBUG:
    # The static() function returns a list of URLPatterns
    static_patterns: List[URLPattern] = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static_patterns
""" urls.py in inspireIA project
URL configuration for inspireIA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from catalog import views as catalog_views
from django.conf import settings
from django.conf.urls.static import static
from .admin import admin_site

urlpatterns = [
    # Admin sites
    path('admin/', admin.site.urls),  # Default admin site (for backward compatibility)
    path('inspire-admin/', admin_site.urls, name='inspire_admin'),  # Custom admin site
    
    # Main pages
    path('', catalog_views.home, name='home'),
    path('catalog/', catalog_views.CatalogView.as_view(), name='catalog'),
    path('catalog/presentation/<uuid:id>/', catalog_views.AIToolDetailView.as_view(), name='presentationAI'),
    path('catalog/compare/', catalog_views.compare_tools, name='compare'),
    
    # User authentication
    path('register/', catalog_views.register_view, name='register'),
    path('login/', catalog_views.login_view, name='login'),
    path('logout/', catalog_views.logout_view, name='logout'),
    path('profile/', catalog_views.profile_view, name='profile'),
    
    # Interaction app - handles chats, favorites, sharing
    path('interaction/', include('interaction.urls')),
    
    # Users app
    path('users/', include('users.urls')),
    
    # Favorites
    path('ai/<uuid:ai_id>/favorite/', catalog_views.toggle_favorite, name='toggle_favorite'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
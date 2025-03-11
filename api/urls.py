"""
API URL Configuration.

This module defines the URL patterns for the API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from typing import List, Union, cast
from django.urls import URLPattern, URLResolver

from .views import catalog, interaction, users

# Create a router for viewsets
router = DefaultRouter()
router.register(r'ai-tools', catalog.AIToolViewSet, basename='ai-tool')
router.register(r'conversations', interaction.ConversationViewSet, basename='conversation')
router.register(r'messages', interaction.MessageViewSet, basename='message')
router.register(r'favorites', interaction.UserFavoriteViewSet, basename='favorite')

# Type hint for URL patterns
urlpatterns: List[Union[URLPattern, URLResolver]] = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/', include('rest_framework.urls')),
    
    # Catalog endpoints
    path('catalog/search/', catalog.search_ai_tools, name='search-ai-tools'),
    path('catalog/categories/', catalog.list_categories, name='list-categories'),
    
    # Interaction endpoints
    path('interaction/chat/<uuid:conversation_id>/', interaction.chat_message, name='chat-message'),
    path('interaction/direct-chat/', interaction.direct_chat_message, name='direct-chat-message'),
    path('interaction/share/<uuid:conversation_id>/', interaction.share_conversation, name='share-conversation'),
    path('interaction/favorite-prompts/', interaction.favorite_prompts, name='favorite-prompts'),
    
    # User endpoints
    path('users/profile/', users.user_profile, name='user-profile'),
]

from django.urls import path, URLPattern, URLResolver
from typing import List, Union
from . import views

# Register the app namespace
app_name = 'interaction'

# Type hint for URL patterns
urlpatterns: List[Union[URLPattern, URLResolver]] = [    
    # Direct chat URLs
    path('direct-chat/', views.direct_chat, name='direct_chat'),
    path('direct-chat/message/', views.direct_chat_message, name='direct_chat_message'),
    # Chat URLs
    path('chat/', views.chat_selection, name='chat_selection'),
    # Important: Order matters! More specific patterns should come first
    path('chat/conversation/<uuid:conversation_id>/', views.chat_view, name='continue_conversation'),
    path('chat/conversation/<uuid:conversation_id>/send/', views.send_message, name='send_message'),
    path('chat/<uuid:ai_id>/', views.chat_view, name='chat'),
    path('conversations/', views.conversation_history, name='conversation_history'),
    path('conversations/<uuid:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('conversations/<uuid:conversation_id>/download/<str:format>/', views.download_conversation, name='download_conversation'),
    
    # Favorite prompts URLs
    path('prompts/', views.favorite_prompts, name='favorite_prompts'),
    path('prompts/ai/<uuid:ai_id>/', views.favorite_prompts, name='ai_favorite_prompts'),
    path('prompts/save/', views.save_favorite_prompt, name='save_favorite_prompt'),
    path('prompts/<uuid:prompt_id>/delete/', views.delete_favorite_prompt, name='delete_favorite_prompt'),
    
    # Sharing URLs
    path('share/<uuid:conversation_id>/', views.share_conversation, name='share_conversation'),
    path('shared/<str:access_token>/', views.view_shared_chat, name='view_shared_chat'),
] 
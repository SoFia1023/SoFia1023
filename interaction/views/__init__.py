"""
Views package for the interaction app.

This package contains all views for the interaction app, organized into logical modules.
"""
# Import views for easy access
from .chat import (
    direct_chat, direct_chat_message, conversation_view, message_view,
    chat_selection, chat_view, send_message
)
from .conversations import (
    conversation_history, delete_conversation, download_conversation
)
from .sharing import share_conversation, view_shared_chat
from .favorites import favorite_prompts, save_favorite_prompt, delete_favorite_prompt

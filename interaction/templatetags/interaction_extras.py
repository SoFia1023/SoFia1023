from django import template
from typing import Any, Dict, List, Optional, Union, cast
from datetime import datetime, timedelta
from django.utils import timezone
from interaction.models import Conversation, Message

# Create a template library instance
register = template.Library()

@register.filter
def format_timestamp(timestamp: datetime) -> str:
    """Format a timestamp in a human-readable format
    
    Args:
        timestamp: The datetime object to format
        
    Returns:
        str: A formatted string representation of the timestamp
    """
    now = timezone.now()
    diff = now - timestamp
    
    if diff < timedelta(minutes=1):
        return "Just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(days=7):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return timestamp.strftime("%b %d, %Y")

@register.filter
def truncate_text(text: str, length: int) -> str:
    """Truncate text to a specified length with ellipsis
    
    Args:
        text: The text to truncate
        length: Maximum length before truncation
        
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + '...'

@register.simple_tag
def get_conversation_stats(user_id: int) -> Dict[str, int]:
    """Get conversation statistics for a user
    
    Args:
        user_id: The ID of the user
        
    Returns:
        Dict[str, int]: Dictionary with conversation statistics
    """
    conversations = Conversation.objects.filter(user_id=user_id)
    total_conversations = conversations.count()
    total_messages = Message.objects.filter(conversation__in=conversations).count()
    
    return {
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'average_messages': int(total_messages / total_conversations) if total_conversations > 0 else 0
    }

@register.inclusion_tag('interaction/tags/message_list.html')
def render_recent_messages(conversation_id: str, limit: int = 5) -> Dict[str, Any]:
    """Render a list of recent messages for a conversation
    
    Args:
        conversation_id: The UUID of the conversation
        limit: Maximum number of messages to include
        
    Returns:
        Dict[str, Any]: Context dictionary with messages
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        # Convert QuerySet to list to match the return type annotation
        messages = list(conversation.get_messages().order_by('-timestamp')[:limit])
        return {'messages': messages}
    except Conversation.DoesNotExist:
        return {'messages': []}

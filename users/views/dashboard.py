"""
Dashboard views for the users app.

This module contains views related to the user dashboard, showing user activity and statistics.
"""
from typing import Any, Dict, Optional, Union
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from interaction.models import Conversation, UserFavorite


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    View for the user dashboard.
    
    This view renders the user's dashboard, showing recent activity and statistics.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered dashboard page
    """
    user = request.user
    
    # Get recent conversations
    recent_conversations = Conversation.objects.filter(
        user=user
    ).order_by('-updated_at')[:5]
    
    # Get favorite AI tools
    favorites = UserFavorite.objects.filter(
        user=user
    ).select_related('ai_tool')
    
    # Get conversation statistics
    total_conversations = Conversation.objects.filter(user=user).count()
    total_messages = sum(
        c.message_set.count() for c in Conversation.objects.filter(user=user)
    )
    
    # Get most used AI tool
    most_used_tool = None
    if total_conversations > 0:
        tool_counts = {}
        for conv in Conversation.objects.filter(user=user):
            if conv.ai_tool:
                tool_name = conv.ai_tool.name
                tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
        
        if tool_counts:
            most_used_tool = max(tool_counts.items(), key=lambda x: x[1])[0]
    
    return render(request, 'users/dashboard.html', {
        'recent_conversations': recent_conversations,
        'favorites': favorites,
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'most_used_tool': most_used_tool
    })

"""
Dashboard views for the users app.

This module contains views related to the user dashboard, showing user activity, statistics,
and profile management.
"""
from typing import Any, Dict, Optional, Union
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from interaction.models import Conversation, UserFavorite
from users.forms import UserProfileForm


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    View for the user dashboard.
    
    This view renders the user's dashboard, showing recent activity, statistics,
    and profile management options. It also handles profile updates.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered dashboard page
    """
    user = request.user
    profile_form = None
    password_form = None
    active_tab = request.GET.get('tab', 'overview')
    
    # Handle profile form submission
    if request.method == 'POST' and 'update_profile' in request.POST:
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:dashboard')
        active_tab = 'profile'
    
    # Handle password form submission
    elif request.method == 'POST' and 'change_password' in request.POST:
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user_updated = password_form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user_updated)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:dashboard')
        active_tab = 'security'
    
    # Initialize forms if not already created
    if profile_form is None:
        profile_form = UserProfileForm(instance=user)
    
    if password_form is None:
        password_form = PasswordChangeForm(user)
    
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
        'most_used_tool': most_used_tool,
        'profile_form': profile_form,
        'password_form': password_form,
        'active_tab': active_tab
    })

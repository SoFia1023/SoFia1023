"""
Sharing views for the interaction app.

This module contains views related to sharing conversations with others.
"""
from typing import Any, Dict, Optional, Union
import json
import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from interaction.models import Conversation, SharedChat, Message

User = get_user_model()


@login_required
@require_http_methods(["POST"])
def share_conversation(request: HttpRequest, conversation_id: uuid.UUID) -> JsonResponse:
    """
    View for sharing a conversation with others.
    
    This view handles creating a shared link for a conversation.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        
    Returns:
        JSON response with the sharing details
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    # Get sharing options from the request
    try:
        data = json.loads(request.body)
        is_public = data.get('is_public', False)
        recipient_username = data.get('recipient_username', '')
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    
    # Generate a unique access token
    access_token = uuid.uuid4().hex
    
    # Create the shared chat
    shared_chat = SharedChat.objects.create(
        conversation=conversation,
        access_token=access_token,
        is_public=is_public,
        created_by=request.user
    )
    
    # If sharing with a specific user, set the recipient
    if recipient_username and not is_public:
        try:
            recipient = User.objects.get(username=recipient_username)
            shared_chat.recipient = recipient
            shared_chat.save(update_fields=['recipient'])
        except User.DoesNotExist:
            return JsonResponse({
                'error': f'User {recipient_username} not found'
            }, status=404)
    
    # Generate the sharing URL
    share_url = f"/interaction/shared/{access_token}/"
    
    return JsonResponse({
        'access_token': access_token,
        'share_url': share_url,
        'is_public': is_public,
        'recipient': recipient_username if not is_public and recipient_username else None
    })


def view_shared_chat(request: HttpRequest, access_token: str) -> HttpResponse:
    """
    View for viewing a shared conversation.
    
    This view renders a shared conversation, accessible via an access token.
    
    Args:
        request: The HTTP request object
        access_token: The access token for the shared conversation
        
    Returns:
        Rendered shared conversation page
    """
    # Get the shared chat
    shared_chat = get_object_or_404(SharedChat, access_token=access_token)
    
    # Check if the user has access
    if not shared_chat.is_public and shared_chat.recipient:
        if not request.user.is_authenticated or request.user != shared_chat.recipient:
            return render(request, 'interaction/shared_access_denied.html')
    
    # Get the conversation
    conversation = shared_chat.conversation
    
    # Get the messages for this conversation
    messages = Message.objects.filter(
        conversation=conversation
    ).order_by('timestamp')
    
    return render(request, 'interaction/shared_conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'shared_by': shared_chat.created_by.username,
        'shared_at': shared_chat.created_at
    })

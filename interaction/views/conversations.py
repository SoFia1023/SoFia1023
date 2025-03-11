"""
Conversations views for the interaction app.

This module contains views related to managing conversations, including listing, deleting, and renaming.
"""
from typing import Any, Dict, Optional, Union
import json
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from core.utils import format_conversation_for_download
from interaction.models import Conversation


@login_required
def conversation_history(request: HttpRequest) -> HttpResponse:
    """
    View for listing the user's conversation history.
    
    This view renders a list of the user's conversations, sorted by last activity.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered conversation history page
    """
    # Get the user's conversations
    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at')
    
    return render(request, 'interaction/conversation_history.html', {
        'conversations': conversations
    })


@login_required
@require_http_methods(["POST"])
def delete_conversation(request: HttpRequest, conversation_id: uuid.UUID) -> JsonResponse:
    """
    View for deleting a conversation.
    
    This view handles deleting a conversation and its messages.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        
    Returns:
        JSON response confirming deletion
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    # Delete the conversation (cascade will delete messages)
    conversation.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Conversation deleted successfully'
    })


@login_required
@require_http_methods(["POST"])
def rename_conversation(request: HttpRequest, conversation_id: uuid.UUID) -> JsonResponse:
    """
    View for renaming a conversation.
    
    This view handles renaming a conversation.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        
    Returns:
        JSON response with the new title
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    # Get the new title from the request
    try:
        data = json.loads(request.body)
        new_title = data.get('title', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    
    if not new_title:
        return JsonResponse({
            'error': 'Title cannot be empty'
        }, status=400)
    
    # Update the conversation title
    conversation.title = new_title
    conversation.save(update_fields=['title'])
    
    return JsonResponse({
        'success': True,
        'title': new_title
    })


@login_required
def download_conversation(request: HttpRequest, conversation_id: uuid.UUID, format: str) -> HttpResponse:
    """
    View for downloading a conversation in various formats.
    
    This view handles downloading a conversation in various formats (txt, json, csv).
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        format: The format to download (txt, json, csv)
        
    Returns:
        HTTP response with the conversation data
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    # Format the conversation for download using the centralized utility function
    content, content_type, file_ext = format_conversation_for_download(conversation, format)
    
    # Prepare the filename
    filename = f"conversation_{conversation_id}.{file_ext}"
    
    # Create the response
    response = HttpResponse(content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

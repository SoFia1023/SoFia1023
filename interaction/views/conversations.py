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
    
    This view handles downloading a conversation in various formats (txt, json, etc.).
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        format: The format to download (txt, json, etc.)
        
    Returns:
        HTTP response with the conversation data
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    # Get the messages for this conversation
    messages = conversation.message_set.all().order_by('timestamp')
    
    # Prepare the filename
    filename = f"conversation_{conversation_id}.{format}"
    
    # Handle different formats
    if format == 'txt':
        # Create a text file
        content = f"Conversation: {conversation.title}\n"
        content += f"AI Tool: {conversation.ai_tool.name if conversation.ai_tool else 'Unknown'}\n"
        content += f"Date: {conversation.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for message in messages:
            sender = "You" if message.is_from_user else conversation.ai_tool.name if conversation.ai_tool else "AI"
            content += f"{sender} ({message.timestamp.strftime('%H:%M:%S')}):\n{message.content}\n\n"
        
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
    elif format == 'json':
        # Create a JSON file
        data = {
            'id': str(conversation.id),
            'title': conversation.title,
            'ai_tool': conversation.ai_tool.name if conversation.ai_tool else None,
            'created_at': conversation.created_at.isoformat(),
            'updated_at': conversation.updated_at.isoformat(),
            'messages': [
                {
                    'id': str(message.id),
                    'content': message.content,
                    'is_from_user': message.is_from_user,
                    'timestamp': message.timestamp.isoformat()
                }
                for message in messages
            ]
        }
        
        response = JsonResponse(data)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
    else:
        # Unsupported format
        return HttpResponse(f"Unsupported format: {format}", status=400)
    
    return response

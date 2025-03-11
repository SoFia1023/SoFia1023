"""
Chat views for the interaction app.

This module contains views related to chatting with AI tools, including direct chat and conversation views.
"""
from typing import Any, Dict, Optional, Union
import json
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from catalog.models import AITool
from catalog.utils import AIService
from interaction.models import Conversation, Message
from interaction.utils import route_message_to_ai_tool


@login_required
def direct_chat(request: HttpRequest) -> HttpResponse:
    """
    View for the direct chat interface.
    
    This view renders the direct chat interface, where users can chat with AI tools
    without explicitly selecting one.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered direct chat page
    """
    # Get the conversation ID from the request, if any
    conversation_id = request.GET.get('conversation_id')
    conversation = None
    messages = []
    
    if conversation_id:
        try:
            # Get the conversation if it exists and belongs to the user
            conversation = Conversation.objects.get(
                id=conversation_id,
                user=request.user
            )
            
            # Get the messages for this conversation
            messages = Message.objects.filter(
                conversation=conversation
            ).order_by('timestamp')
        except (Conversation.DoesNotExist, ValueError):
            # If the conversation doesn't exist or ID is invalid, ignore it
            pass
    
    # Get all AI tools for the tool selector
    ai_tools = AITool.objects.all().order_by('name')
    
    return render(request, 'interaction/direct_chat.html', {
        'conversation': conversation,
        'messages': messages,
        'ai_tools': ai_tools
    })


@login_required
def conversation_view(request: HttpRequest, conversation_id: uuid.UUID) -> HttpResponse:
    """
    View for a specific conversation.
    
    This view renders a specific conversation, showing the message history
    and allowing the user to send new messages.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        
    Returns:
        Rendered conversation page
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    # Get the messages for this conversation
    messages = Message.objects.filter(
        conversation=conversation
    ).order_by('timestamp')
    
    # Get all AI tools for the tool selector
    ai_tools = AITool.objects.all().order_by('name')
    
    return render(request, 'interaction/conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'ai_tools': ai_tools
    })


@login_required
@require_http_methods(["POST"])
def message_view(request: HttpRequest, conversation_id: Optional[uuid.UUID] = None) -> JsonResponse:
    """
    View for sending and receiving messages.
    
    This view handles sending messages to AI tools and receiving responses.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation, if any
        
    Returns:
        JSON response with the AI's reply
    """
    user = request.user
    
    # Get the message content from the request
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        ai_tool_id = data.get('ai_tool_id')
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    
    if not user_message:
        return JsonResponse({
            'error': 'Message cannot be empty'
        }, status=400)
    
    # Get or create the conversation
    conversation = None
    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id, user=user)
        except (Conversation.DoesNotExist, ValueError):
            # If the conversation doesn't exist or ID is invalid, create a new one
            conversation = None
    
    # If no conversation exists, create a new one
    if not conversation:
        # If an AI tool ID is provided, use that tool
        ai_tool = None
        if ai_tool_id:
            try:
                ai_tool = AITool.objects.get(id=ai_tool_id)
            except AITool.DoesNotExist:
                # If the AI tool doesn't exist, use smart routing
                ai_tool = None
        
        # If no AI tool is specified, use smart routing
        if not ai_tool:
            ai_tool, confidence = route_message_to_ai_tool(user_message)
        
        # Create a new conversation with the selected AI tool
        conversation = Conversation.objects.create(
            user=user,
            ai_tool=ai_tool,
            title=user_message[:50] + ('...' if len(user_message) > 50 else '')
        )
    
    # Save the user message
    Message.objects.create(
        conversation=conversation,
        content=user_message,
        is_from_user=True
    )
    
    # Get the AI tool for this conversation
    ai_tool = conversation.ai_tool
    
    # Get the AI service for this tool
    ai_service = AIService(ai_tool)
    
    # Get the AI response
    ai_response = ai_service.get_response(user_message)
    
    # Save the AI response
    ai_message = Message.objects.create(
        conversation=conversation,
        content=ai_response,
        is_from_user=False
    )
    
    # Update the conversation's last activity time
    conversation.updated_at = timezone.now()
    conversation.save(update_fields=['updated_at'])
    
    return JsonResponse({
        'message': ai_response,
        'conversation_id': str(conversation.id),
        'ai_tool_name': ai_tool.name,
        'timestamp': ai_message.timestamp.isoformat()
    })


@login_required
@require_http_methods(["POST"])
def direct_chat_message(request: HttpRequest) -> JsonResponse:
    """
    View for handling direct chat messages.
    
    This view processes messages sent from the direct chat interface,
    routes them to the appropriate AI tool, and returns the AI's response.
    
    Args:
        request: The HTTP request object
        
    Returns:
        JSON response with the AI's reply
    """
    # Get the conversation ID from the request, if any
    conversation_id = request.POST.get('conversation_id')
    
    if conversation_id:
        try:
            # Convert the conversation ID to a UUID
            conversation_uuid = uuid.UUID(conversation_id)
            # Call the message view with the conversation ID
            return message_view(request, conversation_uuid)
        except ValueError:
            # If the conversation ID is invalid, ignore it
            pass
    
    # If no conversation ID is provided or it's invalid, call the message view without it
    return message_view(request)


@login_required
def chat_selection(request: HttpRequest) -> HttpResponse:
    """
    View for selecting an AI tool to chat with.
    
    This view renders the chat selection interface, where users can choose
    which AI tool they want to chat with.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered chat selection page
    """
    # Get all AI tools
    ai_tools = AITool.objects.all().order_by('name')
    
    # Get recent conversations
    recent_conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at')[:5]
    
    return render(request, 'interaction/chat_selection.html', {
        'ai_tools': ai_tools,
        'recent_conversations': recent_conversations
    })


@login_required
def chat_view(request: HttpRequest, ai_id: Optional[uuid.UUID] = None, 
              conversation_id: Optional[uuid.UUID] = None) -> HttpResponse:
    """
    View for the chat interface.
    
    This view renders the chat interface for a specific AI tool or conversation.
    
    Args:
        request: The HTTP request object
        ai_id: The UUID of the AI tool, if starting a new conversation
        conversation_id: The UUID of the conversation, if continuing an existing one
        
    Returns:
        Rendered chat page
    """
    # Initialize variables
    ai_tool = None
    conversation = None
    messages = []
    
    # If a conversation ID is provided, load that conversation
    if conversation_id:
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            user=request.user
        )
        ai_tool = conversation.ai_tool
        messages = Message.objects.filter(
            conversation=conversation
        ).order_by('timestamp')
    # If an AI tool ID is provided, load that tool
    elif ai_id:
        ai_tool = get_object_or_404(AITool, id=ai_id)
    # If neither is provided, redirect to the chat selection page
    else:
        return redirect('interaction:chat_selection')
    
    # Get all AI tools for the tool selector
    ai_tools = AITool.objects.all().order_by('name')
    
    return render(request, 'interaction/chat.html', {
        'ai_tool': ai_tool,
        'conversation': conversation,
        'messages': messages,
        'ai_tools': ai_tools
    })


@login_required
@require_http_methods(["POST"])
def send_message(request: HttpRequest, conversation_id: uuid.UUID) -> JsonResponse:
    """
    View for sending a message in an existing conversation.
    
    This view handles sending a message in an existing conversation and returns the AI's response.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        
    Returns:
        JSON response with the AI's reply
    """
    # Call the message view with the conversation ID
    return message_view(request, conversation_id)

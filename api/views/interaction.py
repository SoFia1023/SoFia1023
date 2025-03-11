"""
API views for the interaction app.

This module contains API views for the interaction app, including viewsets and function-based views.
"""
from typing import Any, Dict, List, Optional, Union, cast
import json
import uuid
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request

from catalog.models import AITool
from interaction.models import Conversation, Message, FavoritePrompt, SharedChat
from interaction.utils import route_message_to_ai_tool
from catalog.utils import AIService


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations.
    
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Return different serializers for list and detail views.
        
        Returns:
            Serializer class appropriate for the request
        """
        from api.serializers.interaction import ConversationSerializer, ConversationDetailSerializer
        
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer
    
    def get_queryset(self) -> Any:
        """
        Return conversations for the current user only.
        
        Returns:
            Queryset of user's conversations
        """
        user = self.request.user
        return Conversation.objects.filter(user=user).order_by('-updated_at')


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages.
    
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = 'api.serializers.interaction.MessageSerializer'
    
    def get_queryset(self) -> Any:
        """
        Return messages for the current user's conversations only.
        
        Returns:
            Queryset of user's messages
        """
        user = self.request.user
        conversation_id = self.request.query_params.get('conversation_id')
        
        if conversation_id:
            return Message.objects.filter(
                conversation__id=conversation_id,
                conversation__user=user
            ).order_by('timestamp')
            
        return Message.objects.filter(
            conversation__user=user
        ).order_by('-timestamp')


class UserFavoriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user favorites.
    
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = 'api.serializers.interaction.UserFavoriteSerializer'
    
    def get_queryset(self) -> Any:
        """
        Return favorites for the current user only.
        
        Returns:
            Queryset of user's favorites
        """
        user = self.request.user
        return user.favorites.all()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def chat_message(request: Request, conversation_id: uuid.UUID) -> Response:
    """
    Send a message in an existing conversation.
    
    Args:
        request: The request object containing the message data
        conversation_id: UUID of the conversation
        
    Returns:
        Response with the AI's reply
    """
    user = request.user
    
    # Get the conversation
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=user)
    except Conversation.DoesNotExist:
        return Response(
            {"error": "Conversation not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get the message content from the request
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON data"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not user_message:
        return Response(
            {"error": "Message cannot be empty"},
            status=status.HTTP_400_BAD_REQUEST
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
    
    return Response({
        "message": ai_response,
        "timestamp": ai_message.timestamp.isoformat()
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def direct_chat_message(request: Request) -> Response:
    """
    Send a message in the direct chat with smart routing.
    
    Args:
        request: The request object containing the message data
        
    Returns:
        Response with the AI's reply and conversation information
    """
    user = request.user
    
    # Get the message content and conversation ID from the request
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON data"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not user_message:
        return Response(
            {"error": "Message cannot be empty"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get or create the conversation
    conversation = None
    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id, user=user)
        except (Conversation.DoesNotExist, ValueError):
            # If the conversation doesn't exist or ID is invalid, create a new one
            conversation = None
    
    # If no conversation exists, create a new one with smart routing
    if not conversation:
        # Route the message to the appropriate AI tool
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
    
    return Response({
        "message": ai_response,
        "conversation_id": str(conversation.id),
        "ai_tool_name": ai_tool.name,
        "timestamp": ai_message.timestamp.isoformat()
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def share_conversation(request: Request, conversation_id: uuid.UUID) -> Response:
    """
    Share a conversation with others.
    
    Args:
        request: The request object containing sharing options
        conversation_id: UUID of the conversation to share
        
    Returns:
        Response with the sharing details
    """
    user = request.user
    
    # Get the conversation
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=user)
    except Conversation.DoesNotExist:
        return Response(
            {"error": "Conversation not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get sharing options from the request
    try:
        data = json.loads(request.body)
        is_public = data.get('is_public', False)
        recipient_username = data.get('recipient_username', '')
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON data"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate a unique access token
    access_token = uuid.uuid4().hex
    
    # Create the shared chat
    shared_chat = SharedChat.objects.create(
        conversation=conversation,
        access_token=access_token,
        is_public=is_public,
        created_by=user
    )
    
    # If sharing with a specific user, set the recipient
    if recipient_username and not is_public:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            recipient = User.objects.get(username=recipient_username)
            shared_chat.recipient = recipient
            shared_chat.save(update_fields=['recipient'])
        except User.DoesNotExist:
            return Response(
                {"error": f"User {recipient_username} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Generate the sharing URL
    share_url = f"/interaction/shared/{access_token}/"
    
    return Response({
        "access_token": access_token,
        "share_url": share_url,
        "is_public": is_public,
        "recipient": recipient_username if not is_public and recipient_username else None
    })


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def favorite_prompts(request: Request) -> Response:
    """
    List or create favorite prompts.
    
    Args:
        request: The request object
        
    Returns:
        Response with favorite prompts or creation confirmation
    """
    user = request.user
    
    if request.method == 'GET':
        # Get favorite prompts for the user
        ai_tool_id = request.query_params.get('ai_tool_id')
        
        queryset = FavoritePrompt.objects.filter(user=user)
        
        # Filter by AI tool if specified
        if ai_tool_id:
            queryset = queryset.filter(ai_tools__id=ai_tool_id)
            
        # Convert to list of dictionaries
        prompts = []
        for prompt in queryset:
            ai_tools_data = [{
                'id': str(tool.id),
                'name': tool.name
            } for tool in prompt.ai_tools.all()]
            
            prompts.append({
                'id': prompt.id,
                'title': prompt.title,
                'content': prompt.prompt_text,
                'ai_tools': ai_tools_data,
                'created_at': prompt.created_at.isoformat()
            })
            
        return Response(prompts)
    
    elif request.method == 'POST':
        # Create a new favorite prompt
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()
            ai_tool_id = data.get('ai_tool_id')
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON data"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not title or not content:
            return Response(
                {"error": "Title and content are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the AI tool if specified
        ai_tool = None
        if ai_tool_id:
            try:
                ai_tool = AITool.objects.get(id=ai_tool_id)
            except AITool.DoesNotExist:
                return Response(
                    {"error": "AI tool not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Create the favorite prompt
        prompt = FavoritePrompt.objects.create(
            user=user,
            title=title,
            prompt_text=content
        )
        
        # Add the AI tool to the prompt's ai_tools if specified
        if ai_tool:
            prompt.ai_tools.add(ai_tool)
        
        ai_tools_data = []
        if ai_tool:
            ai_tools_data = [{
                'id': str(ai_tool.id),
                'name': ai_tool.name
            }]
            
        return Response({
            'id': prompt.id,
            'title': prompt.title,
            'content': prompt.prompt_text,
            'ai_tools': ai_tools_data,
            'created_at': prompt.created_at.isoformat()
        }, status=status.HTTP_201_CREATED)

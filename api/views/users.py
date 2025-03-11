"""
API views for the users app.

This module contains API views for the users app, including viewsets and function-based views.
"""
from typing import Any, Dict, List, Optional, Union, cast
import json
from django.contrib.auth import get_user_model
from django.http import HttpRequest, JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request

from interaction.models import Conversation, UserFavorite

User = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request: Request) -> Response:
    """
    Get the current user's profile information.
    
    Args:
        request: The request object
        
    Returns:
        Response with user profile data
    """
    user = request.user
    
    # Get user's favorite AI tools
    favorites = UserFavorite.objects.filter(user=user)
    favorite_ids = [str(fav.ai_tool.id) for fav in favorites]
    
    # Get user's recent conversations
    recent_conversations = Conversation.objects.filter(user=user).order_by('-updated_at')[:5]
    conversations = []
    
    for conv in recent_conversations:
        conversations.append({
            'id': str(conv.id),
            'title': conv.title,
            'ai_tool_name': conv.ai_tool.name if conv.ai_tool else 'Unknown',
            'updated_at': conv.updated_at.isoformat(),
            'message_count': conv.message_set.count()
        })
    
    # Build the profile data
    profile_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined.isoformat(),
        'favorites_count': len(favorite_ids),
        'favorite_ids': favorite_ids,
        'recent_conversations': conversations
    }
    
    return Response(profile_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request: Request) -> Response:
    """
    Update the current user's profile information.
    
    Args:
        request: The request object containing profile data
        
    Returns:
        Response with updated profile data or error
    """
    user = request.user
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON data"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update user fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'email' in data:
        # Check if email is already taken
        if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
            return Response(
                {"error": "Email is already in use"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.email = data['email']
    
    # Save the user
    user.save()
    
    # Return the updated profile
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined.isoformat()
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request: Request) -> Response:
    """
    Change the current user's password.
    
    Args:
        request: The request object containing old and new passwords
        
    Returns:
        Response with success message or error
    """
    user = request.user
    
    try:
        data = json.loads(request.body)
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON data"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if old password is correct
    if not user.check_password(old_password):
        return Response(
            {"error": "Current password is incorrect"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if new password is valid
    if len(new_password) < 8:
        return Response(
            {"error": "Password must be at least 8 characters long"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Set the new password
    user.set_password(new_password)
    user.save()
    
    return Response({"message": "Password changed successfully"})

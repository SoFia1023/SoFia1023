"""
Profile views for the catalog app.

This module contains views related to user profiles and favorites.
"""
from typing import Any, Dict, Optional, Union
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from catalog.models import AITool
from interaction.models import UserFavorite, Conversation


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    View for displaying the user's profile.
    
    This view renders the user's profile page, including their favorites and conversation history.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered profile page
    """
    user = request.user
    
    # Get user's favorites
    favorites = UserFavorite.objects.filter(user=user).select_related('ai_tool')
    
    # Get user's recent conversations
    recent_conversations = Conversation.objects.filter(user=user).order_by('-updated_at')[:10]
    
    return render(request, 'catalog/profile.html', {
        'user': user,
        'favorites': favorites,
        'recent_conversations': recent_conversations
    })


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request: HttpRequest, pk: int) -> JsonResponse:
    """
    View for toggling an AI tool as a favorite.
    
    This view handles adding or removing an AI tool from the user's favorites.
    
    Args:
        request: The HTTP request object
        pk: The primary key of the AI tool
        
    Returns:
        JSON response with the new favorite status
    """
    user = request.user
    ai_tool = get_object_or_404(AITool, pk=pk)
    
    # Check if the AI tool is already a favorite
    favorite = UserFavorite.objects.filter(user=user, ai_tool=ai_tool).first()
    
    if favorite:
        # Remove from favorites
        favorite.delete()
        is_favorite = False
    else:
        # Add to favorites
        UserFavorite.objects.create(user=user, ai_tool=ai_tool)
        is_favorite = True
    
    return JsonResponse({
        'is_favorite': is_favorite
    })

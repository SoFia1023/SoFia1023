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
from interaction.models import Conversation


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
    favorites = user.favorites.all()
    
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
    is_favorite = user.favorites.filter(id=ai_tool.id).exists()
    
    if is_favorite:
        # Remove from favorites
        user.favorites.remove(ai_tool)
        is_favorite = False
    else:
        # Add to favorites
        user.favorites.add(ai_tool)
        is_favorite = True
    
    return JsonResponse({
        'is_favorite': is_favorite
    })

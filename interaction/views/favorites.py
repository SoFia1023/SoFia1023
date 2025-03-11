"""
Favorites views for the interaction app.

This module contains views related to managing favorite prompts.
"""
from typing import Any, Dict, Optional, Union
import json
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from catalog.models import AITool
from interaction.models import FavoritePrompt


@login_required
def favorite_prompts(request: HttpRequest) -> HttpResponse:
    """
    View for listing the user's favorite prompts.
    
    This view renders a list of the user's favorite prompts.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered favorite prompts page
    """
    # Get the AI tool ID filter, if any
    ai_tool_id = request.GET.get('ai_tool_id')
    
    # Get the user's favorite prompts
    queryset = FavoritePrompt.objects.filter(user=request.user)
    
    # Filter by AI tool if specified
    if ai_tool_id:
        queryset = queryset.filter(ai_tool_id=ai_tool_id)
    
    # Order by creation date
    prompts = queryset.order_by('-created_at')
    
    # Get all AI tools for the filter dropdown
    ai_tools = AITool.objects.all().order_by('name')
    
    return render(request, 'interaction/favorite_prompts.html', {
        'prompts': prompts,
        'ai_tools': ai_tools,
        'selected_ai_tool_id': ai_tool_id
    })


@login_required
@require_http_methods(["POST"])
def save_favorite_prompt(request: HttpRequest) -> JsonResponse:
    """
    View for creating a favorite prompt.
    
    This view handles creating a new favorite prompt.
    
    Args:
        request: The HTTP request object
        
    Returns:
        JSON response with the new prompt details
    """
    # Get the prompt details from the request
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        ai_tool_id = data.get('ai_tool_id')
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    
    if not title or not content:
        return JsonResponse({
            'error': 'Title and content are required'
        }, status=400)
    
    # Get the AI tool if specified
    ai_tool = None
    if ai_tool_id:
        try:
            ai_tool = AITool.objects.get(id=ai_tool_id)
        except AITool.DoesNotExist:
            return JsonResponse({
                'error': 'AI tool not found'
            }, status=404)
    
    # Create the favorite prompt
    prompt = FavoritePrompt.objects.create(
        user=request.user,
        title=title,
        content=content,
        ai_tool=ai_tool
    )
    
    return JsonResponse({
        'id': prompt.id,
        'title': prompt.title,
        'content': prompt.content,
        'ai_tool_id': str(prompt.ai_tool.id) if prompt.ai_tool else None,
        'ai_tool_name': prompt.ai_tool.name if prompt.ai_tool else None,
        'created_at': prompt.created_at.isoformat()
    }, status=201)


@login_required
@require_http_methods(["POST"])
def delete_favorite_prompt(request: HttpRequest, prompt_id: int) -> JsonResponse:
    """
    View for deleting a favorite prompt.
    
    This view handles deleting a favorite prompt.
    
    Args:
        request: The HTTP request object
        prompt_id: The ID of the prompt
        
    Returns:
        JSON response confirming deletion
    """
    # Get the prompt
    prompt = get_object_or_404(
        FavoritePrompt,
        id=prompt_id,
        user=request.user
    )
    
    # Delete the prompt
    prompt.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Prompt deleted successfully'
    })

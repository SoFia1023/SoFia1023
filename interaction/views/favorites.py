"""
Favorites views for the interaction app.

This module contains views related to managing favorite prompts.
"""
from typing import Any, Dict, Optional, Union
import json
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from catalog.models import AITool
from interaction.models import FavoritePrompt
from interaction.forms import FavoritePromptForm


@login_required
def favorite_prompts(request: HttpRequest, ai_id: Optional[uuid.UUID] = None) -> HttpResponse:
    """
    View for listing the user's favorite prompts and creating new ones.
    
    This view renders a list of the user's favorite prompts, optionally filtered by AI tool,
    and handles the creation of new favorite prompts through a form.
    
    Args:
        request: The HTTP request object
        ai_id: Optional UUID of the AI tool to filter by
        
    Returns:
        Rendered favorite prompts page
    """
    # Get the AI tool ID filter, either from the URL parameter or query string
    ai_tool_id = str(ai_id) if ai_id else request.GET.get('ai_tool_id')
    
    # Handle form submission for creating a new favorite prompt
    if request.method == 'POST':
        # Create a new instance but don't save it yet
        new_prompt = FavoritePrompt(user=request.user)
        form = FavoritePromptForm(request.POST, instance=new_prompt)
        
        if form.is_valid():
            prompt = form.save()
            messages.success(request, f'Prompt "{prompt.title}" saved successfully!')
            return redirect('interaction:favorite_prompts')
    else:
        # Initialize an empty form for GET requests
        form = FavoritePromptForm()
    
    # Get the user's favorite prompts
    queryset = FavoritePrompt.objects.filter(user=request.user)
    
    # Filter by AI tool if specified
    if ai_tool_id:
        queryset = queryset.filter(ai_tools__id=ai_tool_id)
    
    # Order by creation date
    prompts_list = queryset.order_by('-created_at')
    
    # Paginate the prompts list
    paginator = Paginator(prompts_list, 12)  # Show 12 prompts per page
    page = request.GET.get('page', 1)
    
    try:
        prompts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        prompts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        prompts = paginator.page(paginator.num_pages)
    
    # Calculate page range to display (show 5 pages around current page)
    current_page = prompts.number
    page_range_start = max(current_page - 2, 1)
    page_range_end = min(current_page + 2, paginator.num_pages)
    
    # Ensure we always show 5 pages if possible
    if page_range_end - page_range_start < 4 and paginator.num_pages > 4:
        if page_range_start == 1:
            page_range_end = min(5, paginator.num_pages)
        elif page_range_end == paginator.num_pages:
            page_range_start = max(paginator.num_pages - 4, 1)
    
    # Get all AI tools for the filter dropdown
    ai_tools = AITool.objects.all().order_by('name')
    
    return render(request, 'interaction/favorite_prompts.html', {
        'prompts': prompts,
        'ai_tools': ai_tools,
        'selected_ai_tool_id': ai_tool_id,
        'form': form,
        'page_obj': prompts,  # For consistent template access
        'paginator': paginator,
        'page_range': range(page_range_start, page_range_end + 1),
        'show_first': page_range_start > 1,
        'show_last': page_range_end < paginator.num_pages
    })


@login_required
@require_http_methods(["POST"])
def save_favorite_prompt(request: HttpRequest) -> JsonResponse:
    """
    View for creating a favorite prompt via AJAX.
    
    This view handles creating a new favorite prompt via AJAX request.
    
    Args:
        request: The HTTP request object
        
    Returns:
        JSON response with the new prompt details or validation errors
    """
    # Get the prompt details from the request
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        prompt_text = data.get('prompt_text', '').strip()
        ai_tool_ids = data.get('ai_tool_ids', [])
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    
    # Create a new instance but don't save it yet
    new_prompt = FavoritePrompt(user=request.user)
    
    # Manually validate the data
    errors = {}
    
    # Validate title
    if not title:
        errors['title'] = ['Title is required.']
    elif len(title) < 3:
        errors['title'] = ['Title must be at least 3 characters long.']
    elif len(title) > 255:
        errors['title'] = ['Title must be less than 255 characters.']
    elif FavoritePrompt.objects.filter(user=request.user, title=title).exists():
        errors['title'] = ['You already have a prompt with this title.']
    
    # Validate prompt_text
    if not prompt_text:
        errors['prompt_text'] = ['Prompt text is required.']
    elif len(prompt_text) < 10:
        errors['prompt_text'] = ['Prompt text should be at least 10 characters long.']
    elif len(prompt_text) > 2000:
        errors['prompt_text'] = ['Prompt text must be less than 2000 characters.']
    
    # Validate AI tools
    valid_ai_tool_ids = []
    if ai_tool_ids:
        for ai_tool_id in ai_tool_ids:
            try:
                ai_tool = AITool.objects.get(id=ai_tool_id)
                valid_ai_tool_ids.append(ai_tool_id)
            except (AITool.DoesNotExist, ValueError, TypeError):
                # Silently ignore invalid AI tool IDs
                pass
    
    # If there are validation errors, return them
    if errors:
        return JsonResponse({
            'errors': errors
        }, status=400)
    
    # Create the favorite prompt
    prompt = FavoritePrompt.objects.create(
        user=request.user,
        title=title,
        prompt_text=prompt_text
    )
    
    # Add the AI tools to the prompt
    if valid_ai_tool_ids:
        prompt.ai_tools.set(valid_ai_tool_ids)
    
    # Get AI tool names for the response
    ai_tool_names = [tool.name for tool in prompt.ai_tools.all()]
    
    return JsonResponse({
        'id': str(prompt.id),  # Convert UUID to string
        'title': prompt.title,
        'prompt_text': prompt.prompt_text,
        'ai_tool_ids': [str(tool.id) for tool in prompt.ai_tools.all()],
        'ai_tool_names': ai_tool_names,
        'created_at': prompt.created_at.isoformat()
    }, status=201)


@login_required
@require_http_methods(["POST"])
def delete_favorite_prompt(request: HttpRequest, prompt_id: uuid.UUID) -> JsonResponse:
    """
    View for deleting a favorite prompt.
    
    This view handles deleting a favorite prompt.
    
    Args:
        request: The HTTP request object
        prompt_id: The UUID of the prompt
        
    Returns:
        JSON response confirming deletion
    """
    try:
        # Get the prompt
        prompt = get_object_or_404(
            FavoritePrompt,
            id=prompt_id,
            user=request.user
        )
        
        # Store the title for the success message
        title = prompt.title
        
        # Delete the prompt
        prompt.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Prompt "{title}" deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
def edit_favorite_prompt(request: HttpRequest, prompt_id: uuid.UUID) -> HttpResponse:
    """
    View for editing a favorite prompt.
    
    This view handles editing an existing favorite prompt.
    
    Args:
        request: The HTTP request object
        prompt_id: The UUID of the prompt to edit
        
    Returns:
        Rendered edit form or redirect to favorite prompts page
    """
    # Get the prompt
    prompt = get_object_or_404(
        FavoritePrompt,
        id=prompt_id,
        user=request.user
    )
    
    if request.method == 'POST':
        form = FavoritePromptForm(request.POST, instance=prompt)
        if form.is_valid():
            form.save()
            messages.success(request, f'Prompt "{prompt.title}" updated successfully!')
            return redirect('interaction:favorite_prompts')
    else:
        form = FavoritePromptForm(instance=prompt)
    
    return render(request, 'interaction/edit_favorite_prompt.html', {
        'form': form,
        'prompt': prompt
    })

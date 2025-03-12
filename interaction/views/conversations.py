"""
Conversations views for the interaction app.

This module contains views related to managing conversations, including listing, deleting, and renaming.
"""
from typing import Any, Dict, Optional, Union
import json
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from catalog.models import AITool
from core.utils import format_conversation_for_download
from interaction.models import Conversation
from interaction.forms import ConversationForm


@login_required
def conversation_history(request: HttpRequest) -> HttpResponse:
    """
    View for listing the user's conversation history and creating new conversations.
    
    This view renders a list of the user's conversations, sorted by last activity,
    and handles the creation of new conversations through a form.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered conversation history page
    """
    # Handle form submission for creating a new conversation
    if request.method == 'POST':
        # Create a new instance but don't save it yet
        new_conversation = Conversation(user=request.user)
        form = ConversationForm(request.POST, instance=new_conversation)
        
        if form.is_valid():
            conversation = form.save()
            messages.success(request, f'Conversation "{conversation.title}" created successfully!')
            # Redirect to the new conversation
            return redirect('interaction:chat', conversation_id=conversation.id)
    else:
        # Initialize an empty form for GET requests
        form = ConversationForm()
    
    # Get the user's conversations
    conversations_list = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at')
    
    # Paginate the conversations list
    paginator = Paginator(conversations_list, 10)  # Show 10 conversations per page
    page = request.GET.get('page', 1)
    
    try:
        conversations = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        conversations = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        conversations = paginator.page(paginator.num_pages)
    
    # Calculate page range to display (show 5 pages around current page)
    current_page = conversations.number
    page_range_start = max(current_page - 2, 1)
    page_range_end = min(current_page + 2, paginator.num_pages)
    
    # Ensure we always show 5 pages if possible
    if page_range_end - page_range_start < 4 and paginator.num_pages > 4:
        if page_range_start == 1:
            page_range_end = min(5, paginator.num_pages)
        elif page_range_end == paginator.num_pages:
            page_range_start = max(paginator.num_pages - 4, 1)
    
    # Get all AI tools for the form dropdown
    ai_tools = AITool.objects.all().order_by('name')
    
    return render(request, 'interaction/conversation_history.html', {
        'conversations': conversations,
        'form': form,
        'ai_tools': ai_tools,
        'page_obj': conversations,  # For consistent template access
        'paginator': paginator,
        'page_range': range(page_range_start, page_range_end + 1),
        'show_first': page_range_start > 1,
        'show_last': page_range_end < paginator.num_pages
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
    
    This view handles renaming a conversation with validation.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        
    Returns:
        JSON response with the new title or validation errors
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
    
    # Validate the title
    errors = {}
    if not new_title:
        errors['title'] = ['Title cannot be empty.']
    elif len(new_title) < 3:
        errors['title'] = ['Title must be at least 3 characters long.']
    elif len(new_title) > 255:
        errors['title'] = ['Title must be less than 255 characters.']
    elif Conversation.objects.filter(user=request.user, title=new_title).exclude(id=conversation_id).exists():
        errors['title'] = ['You already have a conversation with this title.']
    
    # If there are validation errors, return them
    if errors:
        return JsonResponse({
            'errors': errors
        }, status=400)
    
    # Update the conversation title
    conversation.title = new_title
    conversation.save(update_fields=['title', 'updated_at'])
    
    return JsonResponse({
        'success': True,
        'title': new_title,
        'message': f'Conversation renamed to "{new_title}" successfully!'
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


@login_required
def edit_conversation(request: HttpRequest, conversation_id: uuid.UUID) -> HttpResponse:
    """
    View for editing a conversation.
    
    This view handles editing an existing conversation.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation to edit
        
    Returns:
        Rendered edit form or redirect to conversation history page
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    if request.method == 'POST':
        form = ConversationForm(request.POST, instance=conversation)
        if form.is_valid():
            form.save()
            messages.success(request, f'Conversation "{conversation.title}" updated successfully!')
            return redirect('interaction:conversation_history')
    else:
        form = ConversationForm(instance=conversation)
    
    return render(request, 'interaction/edit_conversation.html', {
        'form': form,
        'conversation': conversation
    })

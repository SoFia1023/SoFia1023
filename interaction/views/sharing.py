"""
Sharing views for the interaction app.

This module contains views related to sharing conversations with others.
"""
from typing import Any, Dict, Optional, Union
import json
import uuid
from django.contrib import messages as django_messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from interaction.models import Conversation, SharedChat, Message
from interaction.forms import SharedChatForm

User = get_user_model()


@login_required
def share_conversation_form(request: HttpRequest, conversation_id: uuid.UUID) -> HttpResponse:
    """
    View for rendering and processing the share conversation form.
    
    This view renders the form for sharing a conversation with others and processes form submissions.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        
    Returns:
        Rendered share conversation form or redirect to manage shared chats
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    # Get all users for the recipient dropdown (excluding the current user)
    users = User.objects.exclude(id=request.user.id).order_by('username')
    
    # Handle form submission
    if request.method == 'POST':
        # Create a form instance with the POST data
        form_data = {
            'is_public': request.POST.get('is_public') == 'on',
            'expiration_days': request.POST.get('expiration_days', 7)
        }
        
        # If sharing with a specific user, get the recipient
        recipient_id = request.POST.get('recipient')
        if recipient_id:
            form_data['recipient'] = recipient_id
        
        # Create a form instance with the data
        form = SharedChatForm(form_data)
        
        if form.is_valid():
            # Generate a unique access token
            access_token = uuid.uuid4().hex
            
            # Create the shared chat
            shared_chat = SharedChat.objects.create(
                conversation=conversation,
                access_token=access_token,
                is_public=form.cleaned_data['is_public'],
                created_by=request.user,
                recipient=form.cleaned_data.get('recipient'),
                expiration_days=form.cleaned_data['expiration_days']
            )
            
            # Add a success message
            django_messages.success(
                request, 
                f'Conversation shared successfully. Access token: {access_token}'
            )
            
            # Redirect to the shared chats management page
            return redirect('interaction:manage_shared_chats')
        else:
            # If the form is invalid, add error messages
            for field, errors in form.errors.items():
                for error in errors:
                    django_messages.error(request, f"{field.capitalize()}: {error}")
    
    # Render the form for GET requests or invalid POST submissions
    return render(request, 'interaction/share_conversation.html', {
        'conversation': conversation,
        'users': users
    })


@login_required
def manage_shared_chats(request: HttpRequest) -> HttpResponse:
    """
    View for managing shared chats.
    
    This view displays a list of shared chats for the current user and allows creating new shares.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered manage shared chats page or redirect to the same page after processing a form
    """
    # Get all shared chats created by the current user
    shared_chats = SharedChat.objects.filter(created_by=request.user).select_related(
        'conversation', 'recipient'
    ).order_by('-created_at')
    
    # Get all conversations for the current user for the dropdown
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
    
    # Get all users for the recipient dropdown (excluding the current user)
    users = User.objects.exclude(id=request.user.id).order_by('username')
    
    # Handle form submission for creating a new shared chat
    if request.method == 'POST':
        # Get the conversation ID from the form
        conversation_id = request.POST.get('conversation_id')
        if not conversation_id:
            django_messages.error(request, 'Please select a conversation to share.')
            return redirect('interaction:manage_shared_chats')
        
        # Get the conversation
        try:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        except Conversation.DoesNotExist:
            django_messages.error(request, 'The selected conversation does not exist.')
            return redirect('interaction:manage_shared_chats')
        
        # Create a form instance with the POST data
        form_data = {
            'is_public': request.POST.get('is_public') == 'on',
            'expiration_days': request.POST.get('expiration_days', 7)
        }
        
        # If sharing with a specific user, get the recipient
        recipient_id = request.POST.get('recipient')
        if recipient_id:
            form_data['recipient'] = recipient_id
        
        # Create a form instance with the data
        form = SharedChatForm(form_data)
        
        if form.is_valid():
            # Generate a unique access token
            access_token = uuid.uuid4().hex
            
            # Create the shared chat
            shared_chat = SharedChat.objects.create(
                conversation=conversation,
                access_token=access_token,
                is_public=form.cleaned_data['is_public'],
                created_by=request.user,
                recipient=form.cleaned_data.get('recipient'),
                expiration_days=form.cleaned_data['expiration_days']
            )
            
            # Add a success message
            django_messages.success(
                request, 
                f'Conversation shared successfully. Access token: {access_token}'
            )
            
            # Redirect to the shared chats management page
            return redirect('interaction:manage_shared_chats')
        else:
            # If the form is invalid, add error messages
            for field, errors in form.errors.items():
                for error in errors:
                    django_messages.error(request, f"{field.capitalize()}: {error}")
            return redirect('interaction:manage_shared_chats')
    
    # Render the template for GET requests
    return render(request, 'interaction/manage_shared_chats.html', {
        'shared_chats': shared_chats,
        'conversations': conversations,
        'users': users
    })


@login_required
@require_http_methods(["POST"])
def delete_shared_chat(request: HttpRequest, shared_chat_id: uuid.UUID) -> HttpResponse:
    """
    View for deleting a shared chat.
    
    This view deletes a shared chat and redirects to the manage shared chats page.
    
    Args:
        request: The HTTP request object
        shared_chat_id: The UUID of the shared chat
        
    Returns:
        Redirect to the manage shared chats page
    """
    # Get the shared chat
    shared_chat = get_object_or_404(
        SharedChat,
        id=shared_chat_id,
        created_by=request.user
    )
    
    # Delete the shared chat
    shared_chat.delete()
    
    # Add a success message
    django_messages.success(request, 'Shared conversation deleted successfully.')
    
    # Redirect to the manage shared chats page
    return redirect('interaction:manage_shared_chats')


@login_required
@require_http_methods(["POST"])
def share_conversation(request: HttpRequest, conversation_id: uuid.UUID) -> JsonResponse:
    """
    View for sharing a conversation with others.
    
    This view handles creating a shared link for a conversation with validation.
    
    Args:
        request: The HTTP request object
        conversation_id: The UUID of the conversation
        
    Returns:
        JSON response with the sharing details or validation errors
    """
    # Get the conversation
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    
    # Get sharing options from the request
    try:
        data = json.loads(request.body)
        is_public = data.get('is_public', False)
        recipient_username = data.get('recipient_username', '')
        expiration_days = data.get('expiration_days', 7)  # Default to 7 days
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    
    # Validate the sharing options
    form_data = {
        'is_public': is_public,
        'expiration_days': expiration_days
    }
    
    # If sharing with a specific user, validate the recipient
    recipient = None
    if recipient_username and not is_public:
        try:
            recipient = User.objects.get(username=recipient_username)
            form_data['recipient'] = recipient.id
        except User.DoesNotExist:
            return JsonResponse({
                'error': f'User {recipient_username} not found'
            }, status=404)
    
    # Create a form instance with the data
    form = SharedChatForm(form_data)
    
    # Validate the form
    if not form.is_valid():
        return JsonResponse({
            'errors': form.errors
        }, status=400)
    
    # Generate a unique access token
    access_token = uuid.uuid4().hex
    
    # Create the shared chat
    shared_chat = SharedChat.objects.create(
        conversation=conversation,
        access_token=access_token,
        is_public=form.cleaned_data['is_public'],
        created_by=request.user,
        recipient=form.cleaned_data.get('recipient'),
        expiration_days=form.cleaned_data['expiration_days']
    )
    
    # Generate the sharing URL
    share_url = f"/interaction/shared/{access_token}/"
    
    return JsonResponse({
        'access_token': access_token,
        'share_url': share_url,
        'is_public': shared_chat.is_public,
        'recipient': recipient_username if recipient else None,
        'expiration_days': shared_chat.expiration_days
    })


def view_shared_chat(request: HttpRequest, access_token: str) -> HttpResponse:
    """
    View for viewing a shared conversation.
    
    This view renders a shared conversation, accessible via an access token.
    
    Args:
        request: The HTTP request object
        access_token: The access token for the shared conversation
        
    Returns:
        Rendered shared conversation page or access denied page
    """
    # Get the shared chat
    shared_chat = get_object_or_404(SharedChat, access_token=access_token)
    
    # Check if the shared chat has expired
    if shared_chat.is_expired():
        # Redirect with query parameters for context
        shared_by = shared_chat.created_by.username if shared_chat.created_by else 'Unknown user'
        shared_at = shared_chat.created_at.isoformat() if shared_chat.created_at else None
        
        from django.urls import reverse
        redirect_url = reverse('interaction:shared_expired')
        redirect_url += f"?shared_by={shared_by}&shared_at={shared_at}&expiration_days={shared_chat.expiration_days}"
        return redirect(redirect_url)
    
    # Check if the user has access
    if not shared_chat.is_public and shared_chat.recipient:
        if not request.user.is_authenticated or request.user != shared_chat.recipient:
            # Redirect with query parameters for context
            shared_by = shared_chat.created_by.username if shared_chat.created_by else 'Unknown user'
            shared_at = shared_chat.created_at.isoformat() if shared_chat.created_at else None
            
            from django.urls import reverse
            redirect_url = reverse('interaction:shared_access_denied')
            redirect_url += f"?shared_by={shared_by}&shared_at={shared_at}"
            return redirect(redirect_url)
    
    # Get the conversation
    conversation = shared_chat.conversation
    
    # Get the messages for this conversation
    messages_list = Message.objects.filter(
        conversation=conversation
    ).order_by('timestamp')
    
    return render(request, 'interaction/shared_conversation.html', {
        'conversation': conversation,
        'messages': messages_list,
        'shared_by': shared_chat.created_by.username,
        'shared_at': shared_chat.created_at,
        'expiration_days': shared_chat.expiration_days,
        'is_public': shared_chat.is_public
    })


def shared_conversation(request: HttpRequest, access_token: str) -> HttpResponse:
    """
    View for viewing a shared conversation with the new template.
    
    This view renders a shared conversation, accessible via an access token.
    
    Args:
        request: The HTTP request object
        access_token: The access token for the shared conversation
        
    Returns:
        Rendered shared conversation page or redirect to error pages
    """
    # Get the shared chat or return 404
    shared_chat = get_object_or_404(SharedChat, access_token=access_token)
    
    # Check if the shared chat has expired
    if shared_chat.is_expired():
        # Redirect with query parameters for context
        shared_by = shared_chat.created_by.username if shared_chat.created_by else 'Unknown user'
        shared_at = shared_chat.created_at.isoformat() if shared_chat.created_at else None
        
        from django.urls import reverse
        redirect_url = reverse('interaction:shared_expired')
        redirect_url += f"?shared_by={shared_by}&shared_at={shared_at}&expiration_days={shared_chat.expiration_days}"
        return redirect(redirect_url)
    
    # Check if the user has access to the shared chat
    if not shared_chat.is_public and shared_chat.recipient:
        if not request.user.is_authenticated or request.user != shared_chat.recipient:
            # Redirect with query parameters for context
            shared_by = shared_chat.created_by.username if shared_chat.created_by else 'Unknown user'
            shared_at = shared_chat.created_at.isoformat() if shared_chat.created_at else None
            
            from django.urls import reverse
            redirect_url = reverse('interaction:shared_access_denied')
            redirect_url += f"?shared_by={shared_by}&shared_at={shared_at}"
            return redirect(redirect_url)
    
    # Get the conversation and messages
    conversation = shared_chat.conversation
    messages_list = Message.objects.filter(conversation=conversation).order_by('timestamp')
    
    # Render the shared conversation template
    return render(request, 'interaction/shared_conversation.html', {
        'conversation': conversation,
        'messages': messages_list,
        'shared_by': shared_chat.created_by.username,
        'shared_at': shared_chat.created_at,
        'expiration_days': shared_chat.expiration_days,
        'is_public': shared_chat.is_public
    })


def shared_expired(request: HttpRequest) -> HttpResponse:
    """
    View for displaying a message when a shared conversation has expired.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered shared expired page with context information
    """
    # Get query parameters
    shared_by = request.GET.get('shared_by', 'Unknown user')
    shared_at_str = request.GET.get('shared_at')
    expiration_days = int(request.GET.get('expiration_days', '7'))
    
    # Parse shared_at date if provided
    shared_at = None
    expired_at = None
    if shared_at_str:
        try:
            shared_at = timezone.datetime.fromisoformat(shared_at_str)
            # Calculate expiration date
            expired_at = shared_at + timezone.timedelta(days=expiration_days)
        except (ValueError, TypeError):
            # If date parsing fails, we'll use None values
            pass
    
    context = {
        'shared_by': shared_by,
        'shared_at': shared_at,
        'expired_at': expired_at,
        'expiration_days': expiration_days
    }
    
    return render(request, 'interaction/shared_expired.html', context)


def shared_access_denied(request: HttpRequest) -> HttpResponse:
    """
    View for displaying a message when access to a shared conversation is denied.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered access denied page with context information
    """
    # Get query parameters
    shared_by = request.GET.get('shared_by', 'Unknown user')
    shared_at_str = request.GET.get('shared_at')
    
    # Parse shared_at date if provided
    shared_at = None
    if shared_at_str:
        try:
            shared_at = timezone.datetime.fromisoformat(shared_at_str)
        except (ValueError, TypeError):
            # If date parsing fails, we'll use None
            pass
    
    context = {
        'shared_by': shared_by,
        'shared_at': shared_at
    }
    
    return render(request, 'interaction/shared_access_denied.html', context)


@login_required
def manage_shared_chats(request: HttpRequest) -> HttpResponse:
    """
    View for managing shared chats.
    
    This view allows users to view and manage their shared conversations.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered shared chats management page
    """
    # Get all shared chats created by the user
    shared_chats = SharedChat.objects.filter(
        created_by=request.user
    ).order_by('-created_at')
    
    # Handle form submission for creating a new shared chat
    if request.method == 'POST':
        # Get the conversation ID from the form
        conversation_id = request.POST.get('conversation_id')
        
        try:
            # Get the conversation
            conversation = Conversation.objects.get(
                id=conversation_id,
                user=request.user
            )
            
            # Create a form instance with the POST data
            form = SharedChatForm(request.POST)
            
            if form.is_valid():
                # Generate a unique access token
                access_token = uuid.uuid4().hex
                
                # Create the shared chat
                shared_chat = SharedChat.objects.create(
                    conversation=conversation,
                    access_token=access_token,
                    is_public=form.cleaned_data['is_public'],
                    created_by=request.user,
                    recipient=form.cleaned_data.get('recipient'),
                    expiration_days=form.cleaned_data['expiration_days']
                )
                
                # Add a success message
                django_messages.success(
                    request, 
                    f'Conversation shared successfully. Access token: {access_token}'
                )
                
                # Redirect to avoid form resubmission
                return redirect('interaction:manage_shared_chats')
            else:
                # If the form is invalid, add error messages
                for field, errors in form.errors.items():
                    for error in errors:
                        django_messages.error(request, f"{field.capitalize()}: {error}")
        except Conversation.DoesNotExist:
            # If the conversation doesn't exist, add an error message
            django_messages.error(request, 'Conversation not found')
    else:
        # Initialize an empty form for GET requests
        form = SharedChatForm()
    
    # Get all conversations for the user
    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at')
    
    return render(request, 'interaction/manage_shared_chats.html', {
        'shared_chats': shared_chats,
        'conversations': conversations,
        'form': form
    })


@login_required
@require_http_methods(["POST"])
def delete_shared_chat(request: HttpRequest, shared_chat_id: uuid.UUID) -> HttpResponse:
    """
    View for deleting a shared chat.
    
    This view handles deleting a shared chat.
    
    Args:
        request: The HTTP request object
        shared_chat_id: The UUID of the shared chat
        
    Returns:
        Redirect to the shared chats management page
    """
    # Get the shared chat
    shared_chat = get_object_or_404(
        SharedChat,
        id=shared_chat_id,
        created_by=request.user
    )
    
    # Delete the shared chat
    shared_chat.delete()
    
    # Add a success message
    django_messages.success(request, 'Shared chat deleted successfully')
    
    # Redirect to the shared chats management page
    return redirect('interaction:manage_shared_chats')

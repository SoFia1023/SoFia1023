from django.shortcuts import render
import uuid
import json
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

from catalog.models import AITool
from .models import Conversation, Message, FavoritePrompt, SharedChat
from catalog.utils import call_openai_api, call_huggingface_api

# Create your views here.

# Chat views
@login_required
def chat_selection(request):
    """View to select an AI tool to chat with."""
    ai_tools = AITool.objects.filter(
        Q(api_type='openai') | Q(api_type='huggingface') | Q(api_type='custom')
    ).order_by('name')
    
    # Get user's recent conversations
    recent_conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at')[:5]
    
    return render(request, 'interaction/chat_selection.html', {
        'ai_tools': ai_tools,
        'recent_conversations': recent_conversations
    })

@login_required
def chat_view(request, ai_id=None, conversation_id=None):
    """View for chatting with an AI tool."""
    # If conversation_id is provided, load that conversation
    if conversation_id:
        conversation = get_object_or_404(
            Conversation, 
            id=conversation_id,
            user=request.user
        )
        ai_tool = conversation.ai_tool
        messages = conversation.get_messages()
    else:
        # Otherwise, start a new conversation with the specified AI
        ai_tool = get_object_or_404(AITool, id=ai_id)
        conversation = Conversation.objects.create(
            user=request.user,
            ai_tool=ai_tool,
            title=f"Chat with {ai_tool.name}"
        )
        messages = []
    
    # Get user's favorite prompts for this AI tool
    favorite_prompts = FavoritePrompt.objects.filter(
        user=request.user,
        ai_tool=ai_tool
    ).order_by('-created_at')
    
    return render(request, 'interaction/chat.html', {
        'ai_tool': ai_tool,
        'conversation': conversation,
        'messages': messages,
        'favorite_prompts': favorite_prompts
    })

@login_required
@require_POST
def send_message(request, conversation_id):
    """Handle sending a message in a conversation."""
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id,
        user=request.user
    )
    
    # Get message from request
    data = json.loads(request.body)
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    
    # Save user message
    Message.objects.create(
        conversation=conversation,
        content=user_message,
        is_user=True
    )
    
    # Update conversation timestamp
    conversation.updated_at = timezone.now()
    conversation.save()
    
    # Process with appropriate API based on AI tool type
    ai_tool = conversation.ai_tool
    ai_response = ""
    
    if ai_tool.api_type == 'openai':
        response = call_openai_api(user_message)
        if response.get('success'):
            ai_response = response['data']['choices'][0]['text'].strip()
        else:
            ai_response = f"Error: {response.get('error', 'Unknown error')}"
    
    elif ai_tool.api_type == 'huggingface':
        model = ai_tool.api_model or "google/flan-t5-small"
        response = call_huggingface_api(user_message, model)
        if response.get('success'):
            ai_response = response['data'][0]['generated_text'].strip()
        else:
            ai_response = f"Error: {response.get('error', 'Unknown error')}"
    
    elif ai_tool.api_type == 'custom':
        # Placeholder for custom API integration
        ai_response = "This is a placeholder response for custom API integration."
    
    else:
        ai_response = "This AI tool does not have API integration configured."
    
    # Save AI response
    Message.objects.create(
        conversation=conversation,
        content=ai_response,
        is_user=False
    )
    
    return JsonResponse({
        'message': ai_response,
        'timestamp': timezone.now().isoformat()
    })

@login_required
def conversation_history(request):
    """View user's conversation history."""
    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at')
    
    return render(request, 'interaction/conversation_history.html', {
        'conversations': conversations
    })

@login_required
def delete_conversation(request, conversation_id):
    """Delete a conversation."""
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id,
        user=request.user
    )
    
    if request.method == 'POST':
        conversation.delete()
        messages.success(request, "Conversation deleted successfully.")
        return redirect('conversation_history')
    
    return render(request, 'interaction/delete_conversation.html', {
        'conversation': conversation
    })

@login_required
def download_conversation(request, conversation_id, format):
    """Download a conversation in various formats."""
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id,
        user=request.user
    )
    
    if format == 'json':
        response = HttpResponse(
            conversation.to_json(),
            content_type='application/json'
        )
        filename = f"conversation_{conversation.id}.json"
    
    elif format == 'txt':
        # Create plain text version
        content = f"Conversation: {conversation.title}\n"
        content += f"AI Tool: {conversation.ai_tool.name}\n"
        content += f"Date: {conversation.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for msg in conversation.get_messages():
            sender = "You" if msg.is_user else conversation.ai_tool.name
            content += f"{sender} ({msg.timestamp.strftime('%H:%M')}): {msg.content}\n\n"
        
        response = HttpResponse(content, content_type='text/plain')
        filename = f"conversation_{conversation.id}.txt"
    
    else:
        return JsonResponse({'error': 'Invalid format'}, status=400)
    
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

# Favorite prompts views
@login_required
def favorite_prompts(request, ai_id=None):
    """View and manage favorite prompts."""
    if ai_id:
        ai_tool = get_object_or_404(AITool, id=ai_id)
        prompts = FavoritePrompt.objects.filter(
            user=request.user,
            ai_tool=ai_tool
        ).order_by('-created_at')
    else:
        ai_tool = None
        prompts = FavoritePrompt.objects.filter(
            user=request.user
        ).order_by('-created_at')
    
    ai_tools = AITool.objects.all().order_by('name')
    
    return render(request, 'interaction/favorite_prompts.html', {
        'prompts': prompts,
        'ai_tools': ai_tools,
        'selected_ai': ai_tool
    })

@login_required
@require_POST
def save_favorite_prompt(request):
    """Save a prompt as favorite."""
    data = json.loads(request.body)
    ai_id = data.get('ai_id')
    prompt_text = data.get('prompt_text', '').strip()
    title = data.get('title', '').strip()
    
    if not all([ai_id, prompt_text, title]):
        return JsonResponse({'error': 'All fields are required'}, status=400)
    
    ai_tool = get_object_or_404(AITool, id=ai_id)
    
    FavoritePrompt.objects.create(
        user=request.user,
        ai_tool=ai_tool,
        prompt_text=prompt_text,
        title=title
    )
    
    return JsonResponse({'success': True})

@login_required
def delete_favorite_prompt(request, prompt_id):
    """Delete a favorite prompt."""
    prompt = get_object_or_404(
        FavoritePrompt, 
        id=prompt_id,
        user=request.user
    )
    
    if request.method == 'POST':
        prompt.delete()
        messages.success(request, "Prompt deleted successfully.")
        return redirect('favorite_prompts')
    
    return render(request, 'interaction/delete_prompt.html', {
        'prompt': prompt
    })

# Sharing views
@login_required
def share_conversation(request, conversation_id):
    """Share a conversation with others."""
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id,
        user=request.user
    )
    
    if request.method == 'POST':
        is_public = request.POST.get('is_public') == 'on'
        shared_with_username = request.POST.get('shared_with', '').strip()
        
        # Generate a secure access token
        access_token = secrets.token_urlsafe(32)
        
        shared_chat = SharedChat(
            conversation=conversation,
            shared_by=request.user,
            is_public=is_public,
            access_token=access_token
        )
        
        # If sharing with a specific user
        if shared_with_username and not is_public:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            try:
                shared_with_user = User.objects.get(username=shared_with_username)
                shared_chat.shared_with = shared_with_user
            except User.DoesNotExist:
                messages.error(request, f"User '{shared_with_username}' not found.")
                return redirect('share_conversation', conversation_id=conversation_id)
        
        shared_chat.save()
        
        # Generate share URL
        share_url = request.build_absolute_uri(
            reverse('view_shared_chat', kwargs={'access_token': access_token})
        )
        
        return render(request, 'interaction/share_success.html', {
            'conversation': conversation,
            'share_url': share_url,
            'is_public': is_public,
            'shared_with': shared_chat.shared_with
        })
    
    return render(request, 'interaction/share_conversation.html', {
        'conversation': conversation
    })

def view_shared_chat(request, access_token):
    """View a shared conversation."""
    shared_chat = get_object_or_404(SharedChat, access_token=access_token)
    conversation = shared_chat.conversation
    
    # Check if this is a private share and the user is authorized
    if not shared_chat.is_public and shared_chat.shared_with:
        if not request.user.is_authenticated or request.user != shared_chat.shared_with:
            return render(request, 'interaction/access_denied.html')
    
    messages = conversation.get_messages()
    
    return render(request, 'interaction/view_shared_chat.html', {
        'conversation': conversation,
        'messages': messages,
        'shared_by': shared_chat.shared_by
    })

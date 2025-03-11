from django.shortcuts import render
import uuid
import json
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from typing import Dict, Any, List, Optional, Union, Type, TypeVar, cast, Tuple
from django.db.models.query import QuerySet

from catalog.models import AITool
from .models import Conversation, Message, FavoritePrompt, SharedChat
from .utils import format_conversation_for_download, route_message_to_ai_tool
from catalog.utils import AIService

# Create your views here.

# Available categories for AI tools
CATEGORIES = ["Text Generator", "Image Generator", "Video Generator", "Transcription", "Word Processor", "Code Generator", "AI Platform"]

# Direct chat view
@login_required
def direct_chat(request: HttpRequest) -> HttpResponse:
    """
    View for the smart chat interface that routes messages to appropriate AI tools.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session and GET parameters
        
    Returns:
        HttpResponse: Rendered direct chat template with conversation context
    """
    
    conversation_id = request.GET.get('conversation_id')
    
    if conversation_id:
        # Load existing conversation if ID is provided
        try:
            conversation = get_object_or_404(
                Conversation, 
                id=conversation_id,
                user=request.user
            )
            messages = list(conversation.get_messages())
            
            # Get the AI tool name for display
            ai_tool_name = conversation.ai_tool.name
        except:
            # If conversation not found, start fresh
            conversation = None
            messages = []
            ai_tool_name = "AI Assistant"
    else:
        # Start fresh with no conversation
        conversation = None
        messages = []
        ai_tool_name = "AI Assistant"
    
    return render(request, 'interaction/direct_chat.html', {
        'conversation': conversation,
        'messages': messages,
        'ai_tool_name': ai_tool_name
    })

@login_required
@require_POST
def direct_chat_message(request: HttpRequest) -> JsonResponse:
    """
    Handle sending a message in the direct chat interface with smart routing.
    
    This function processes a user message, determines the appropriate AI tool to handle it,
    creates or updates a conversation, and returns the AI's response.
    
    Args:
        request (HttpRequest): The HTTP request object containing the message data in JSON format
        
    Returns:
        JsonResponse: JSON containing the AI response, conversation ID, and AI tool name,
                     or error information if processing failed
    """
    
    try:
        # STEP 1: PARSE AND VALIDATE INPUT DATA
        # Extract the message content and conversation ID from the request body
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        # Validate that the message is not empty
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # STEP 2: CONVERSATION HANDLING LOGIC
        # There are two possible paths: continue existing conversation or start a new one
        if conversation_id:
            # CASE 2A: EXISTING CONVERSATION
            # Try to retrieve the existing conversation and its associated AI tool
            try:
                # Ensure the conversation exists and belongs to the current user (security check)
                conversation = get_object_or_404(
                    Conversation, 
                    id=conversation_id,
                    user=request.user  # Important security check to prevent accessing others' conversations
                )
                ai_tool = conversation.ai_tool
            except:
                # FALLBACK: If conversation not found or doesn't belong to user,
                # treat this as a new conversation and find appropriate AI tool
                ai_tool = route_message_to_ai_tool(user_message)
                
                # FALLBACK CHAIN: Multiple levels of fallback to ensure we always have a tool
                if ai_tool is None:
                    # Primary fallback: Use the most popular tool in the database
                    ai_tool = AITool.objects.first()
                    # Secondary fallback: Check if we have any tools at all
                    if ai_tool is None:
                        return JsonResponse({'error': 'No AI tools available'}, status=500)
                
                # Create a new conversation with the selected/fallback tool
                # Use a safe accessor pattern for the tool name in case of custom tool objects
                tool_name = ai_tool.name if hasattr(ai_tool, 'name') else "AI Tool"
                conversation = Conversation.objects.create(
                    user=request.user,
                    ai_tool=ai_tool,
                    title=f"Chat with {tool_name}"  # Generate a default title
                )
        else:
            # CASE 2B: NEW CONVERSATION
            # Route the message to the most appropriate AI tool based on content analysis
            ai_tool = route_message_to_ai_tool(user_message)
            
            # Apply the same fallback chain as above
            if ai_tool is None:
                ai_tool = AITool.objects.first()
                if ai_tool is None:
                    return JsonResponse({'error': 'No AI tools available'}, status=500)
            
            # Create a fresh conversation with the selected AI tool
            tool_name = ai_tool.name if hasattr(ai_tool, 'name') else "AI Tool"
            conversation = Conversation.objects.create(
                user=request.user,
                ai_tool=ai_tool,
                title=f"Chat with {tool_name}"
            )
        
        # STEP 3: SAVE USER MESSAGE
        # Record the user's message in the database to maintain conversation history
        Message.objects.create(
            conversation=conversation,
            content=user_message,
            is_user=True  # Flag indicating this is a user message, not an AI response
        )
        
        # Update the conversation's timestamp to reflect the latest activity
        # This is used for sorting conversations by recency
        conversation.updated_at = timezone.now()
        conversation.save()
        
        # STEP 4: PREPARE AI SERVICE CONFIGURATION
        # Extract the necessary configuration from the AI tool for API calls
        service_config = {
            'api_type': ai_tool.api_type,      # Which AI service to use (e.g., 'openai', 'huggingface')
            'api_model': ai_tool.api_model,    # Which model to use within that service
            'api_endpoint': ai_tool.api_endpoint  # Custom endpoint if applicable
        }
        
        # STEP 5: SEND MESSAGE TO AI SERVICE AND PROCESS RESPONSE
        try:
            # Call the AI service with the user's message and tool configuration
            ai_response = AIService.send_to_ai_service(user_message, service_config)
            
            # Check if the AI service call was successful
            if ai_response.get('success'):
                # CASE 5A: SUCCESSFUL AI RESPONSE
                # Save the AI's response to the conversation history
                ai_message = Message.objects.create(
                    conversation=conversation,
                    content=ai_response.get('data'),  # The actual response text
                    is_user=False  # Flag indicating this is an AI response
                )
                
                # Update conversation timestamp again to reflect the AI's response
                conversation.updated_at = timezone.now()
                conversation.save()
                
                # Increment the AI tool's popularity counter
                # This helps track which tools are most used and successful
                ai_tool.popularity += 1
                ai_tool.save()
                
                # Return the successful response to the client
                return JsonResponse({
                    'response': ai_response.get('data'),  # AI's response text
                    'conversation_id': str(conversation.id),  # For continued conversation
                    'ai_tool_name': ai_tool.name  # For UI display
                })
            else:
                # CASE 5B: AI SERVICE ERROR
                # Return the error from the AI service to the client
                return JsonResponse({
                    'error': ai_response.get('error', 'An error occurred with the AI service'),
                    'conversation_id': str(conversation.id),
                    'ai_tool_name': ai_tool.name
                })
        except Exception as e:
            # CASE 5C: UNEXPECTED ERROR DURING AI PROCESSING
            # Catch and return any exceptions that occur during AI service interaction
            return JsonResponse({
                'error': f"Error processing message: {str(e)}",
                'conversation_id': str(conversation.id),
                'ai_tool_name': ai_tool.name
            })
    except json.JSONDecodeError:
        # CASE: MALFORMED JSON INPUT
        # Handle invalid JSON in the request body
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        # CASE: UNEXPECTED GENERAL ERROR
        # Catch-all for any other exceptions to prevent server crashes
        return JsonResponse({'error': f"Unexpected error: {str(e)}"}, status=500)

# Chat views
@login_required
def chat_selection(request: HttpRequest) -> HttpResponse:
    """
    View to select an AI tool to chat with.
    
    This function displays available AI tools with filtering and sorting options.
    
    Args:
        request (HttpRequest): The HTTP request object containing filter parameters
        
    Returns:
        HttpResponse: Rendered template with filtered and sorted AI tools
    """
    
    # Get filter parameters from request
    searchTerm = request.GET.get('searchAITool', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', '')
    
    # Start with AI tools that have API integration
    ai_tools = AITool.objects.filter(
        Q(api_type='openai') | Q(api_type='huggingface') | Q(api_type='custom')
    )
    
    # Apply category filter if provided and valid
    if category in CATEGORIES:
        ai_tools = ai_tools.filter(category=category)
    
    # Apply search filter if provided (search in name, provider, and description)
    if searchTerm:
        ai_tools = ai_tools.filter(
            Q(name__icontains=searchTerm) | 
            Q(provider__icontains=searchTerm) | 
            Q(description__icontains=searchTerm)
        )
    
    # Apply sorting if provided
    if sort:
        if sort == 'popularity_desc':
            ai_tools = ai_tools.order_by('-popularity')
        elif sort == 'popularity_asc':
            ai_tools = ai_tools.order_by('popularity')
        elif sort == 'name_asc':
            ai_tools = ai_tools.order_by('name')
        elif sort == 'name_desc':
            ai_tools = ai_tools.order_by('-name')
    else:
        # Default sorting by popularity (highest first)
        ai_tools = ai_tools.order_by('-popularity')
    
    # Get the featured AI (highest popularity)
    featured_ai = AITool.objects.filter(
        Q(api_type='openai') | Q(api_type='huggingface') | Q(api_type='custom')
    ).order_by('-popularity').first()
    
    # Get user's recent conversations
    recent_conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at')[:5]
    
    return render(request, 'interaction/chat_selection.html', {
        'ai_tools': ai_tools,
        'categories': CATEGORIES,
        'searchTerm': searchTerm,
        'current_category': category,
        'sort': sort,
        'featured_ai': featured_ai,
        'recent_conversations': recent_conversations
    })

@login_required
def chat_view(request: HttpRequest, ai_id: Optional[int] = None, conversation_id: Optional[str] = None) -> HttpResponse:
    """
    View for chatting with an AI tool.
    
    This function either loads an existing conversation or creates a new one with the specified AI tool.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session
        ai_id (Optional[int]): ID of the AI tool to chat with, required when starting a new conversation
        conversation_id (Optional[str]): UUID of an existing conversation to load
        
    Returns:
        HttpResponse: Rendered chat template with conversation context
    """
    
    # Debug logging
    print(f"[CHAT] chat_view called with ai_id={ai_id}, conversation_id={conversation_id}")
    
    # If conversation_id is provided, load that conversation
    if conversation_id:
        print(f"[CHAT] Loading existing conversation with ID: {conversation_id}")
        
        # Get the conversation
        conversation = get_object_or_404(
            Conversation, 
            id=conversation_id,
            user=request.user
        )
        
        # Get associated AI tool
        ai_tool = conversation.ai_tool
        
        # Get messages
        messages = list(conversation.get_messages())
        print(f"[CHAT] Loaded {len(messages)} messages from conversation")
        for i, msg in enumerate(messages):
            print(f"[CHAT] Message {i+1}: {msg.content[:30]}... (User: {msg.is_user})")
    else:
        # Otherwise, start a new conversation with the specified AI
        print(f"[CHAT] Starting new conversation with AI tool ID: {ai_id}")
        
        # Get the AI tool
        ai_tool = get_object_or_404(AITool, id=ai_id)
        
        # Create a new conversation
        conversation = Conversation.objects.create(
            user=request.user,
            ai_tool=ai_tool,
            title=f"Chat with {ai_tool.name}"
        )
        
        print(f"[CHAT] Created new conversation with ID: {conversation.id}")
        messages = []
    
    # Get user's favorite prompts for this AI tool
    favorite_prompts = FavoritePrompt.objects.filter(
        user=request.user,
        ai_tool=ai_tool
    ).order_by('-created_at')
    
    # Ensure conversation ID is properly passed to the template
    context = {
        'ai_tool': ai_tool,
        'conversation': conversation,
        'messages': messages,
        'favorite_prompts': favorite_prompts,
        'conversation_id': str(conversation.id)  # Explicitly pass conversation ID as string
    }
    
    print(f"[CHAT] Rendering chat.html with conversation_id={context['conversation_id']} and {len(messages)} messages")
    return render(request, 'interaction/chat.html', context)

@login_required
@require_POST
def send_message(request: HttpRequest, conversation_id: str) -> JsonResponse:
    """
    Handle sending a message in a conversation.
    
    This function processes a user message in an existing conversation, sends it to the appropriate
    AI service, and returns the AI's response.
    
    Args:
        request (HttpRequest): The HTTP request object containing the message data in JSON format
        conversation_id (str): UUID of the conversation to send the message to
        
    Returns:
        JsonResponse: JSON containing the AI response and timestamp, or error information
    """
    
    # Add debug logging
    print(f"[CHAT] Received message request for conversation {conversation_id}")
    
    try:
        conversation = get_object_or_404(
            Conversation, 
            id=conversation_id,
            user=request.user
        )
        
        # Get message from request
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            print(f"[CHAT] Message content: {user_message}")
            
            if not user_message:
                print("[CHAT] Error: Empty message")
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        except json.JSONDecodeError as e:
            print(f"[CHAT] Error decoding JSON: {str(e)}")
            return JsonResponse({'error': f'Invalid JSON format: {str(e)}'}, status=400)
        
        # Save user message
        try:
            Message.objects.create(
                conversation=conversation,
                content=user_message,
                is_user=True
            )
            
            # Update conversation timestamp
            conversation.updated_at = timezone.now()
            conversation.save()
            print(f"[CHAT] User message saved successfully")
        except Exception as e:
            print(f"[CHAT] Error saving user message: {str(e)}")
            return JsonResponse({'error': f'Error saving message: {str(e)}'}, status=500)
        
        # Process with appropriate API based on AI tool type
        ai_tool = conversation.ai_tool
        
        # Prepare service configuration
        service_config = {
            'api_type': ai_tool.api_type,
            'api_model': ai_tool.api_model,
            'api_endpoint': ai_tool.api_endpoint
        }
        
        print(f"[CHAT] Using service config: {service_config}")
        
        # Send message to AI service
        try:
            print(f"[CHAT] Sending message to AI service")
            response = AIService.send_to_ai_service(user_message, service_config)
            print(f"[CHAT] AI service response received")
        except Exception as e:
            print(f"[CHAT] Error calling AI service: {str(e)}")
            return JsonResponse({'error': f'Error calling AI service: {str(e)}'}, status=500)
        
        if response.get('success'):
            ai_response = response.get('data', '')
            print(f"[CHAT] Successfully got AI response with {len(ai_response)} characters")
        else:
            error_msg = response.get('error', 'An error occurred while processing your request.')
            print(f"[CHAT] AI service error: {error_msg}")
            ai_response = f"Error: {error_msg}"
        
        # Save AI response
        try:
            ai_message = Message.objects.create(
                conversation=conversation,
                content=ai_response,
                is_user=False
            )
            print(f"[CHAT] AI response saved to database")
        except Exception as e:
            print(f"[CHAT] Error saving AI response: {str(e)}")
            return JsonResponse({'error': f'Error saving AI response: {str(e)}'}, status=500)
        
        # Format the timestamp for display
        timestamp = ai_message.timestamp.strftime('%H:%M')
        
        return JsonResponse({
            'success': True,
            'message': ai_response,
            'timestamp': timestamp
        })
    except Exception as e:
        print(f"[CHAT] Unexpected error in send_message: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

@login_required
def conversation_history(request: HttpRequest) -> HttpResponse:
    """
    View user's conversation history.
    
    This function retrieves and displays all conversations for the current user.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session
        
    Returns:
        HttpResponse: Rendered template with the user's conversation history
    """
    
    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at')
    
    return render(request, 'interaction/conversation_history.html', {
        'conversations': conversations
    })

@login_required
def delete_conversation(request: HttpRequest, conversation_id: str) -> HttpResponse:
    """
    Delete a conversation.
    
    This function handles the deletion of a conversation, with confirmation page.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session
        conversation_id (str): UUID of the conversation to delete
        
    Returns:
        HttpResponse: Redirect to conversation history on successful deletion,
                     or confirmation page on GET request
    """
    
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
def download_conversation(request: HttpRequest, conversation_id: str, format: str = 'json') -> HttpResponse:
    """
    Download a conversation in various formats.
    
    This function formats and returns a conversation in the specified format for download.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session
        conversation_id (str): UUID of the conversation to download
        format (str): Format to download the conversation in ('json', 'txt', or 'csv')
        
    Returns:
        HttpResponse: HTTP response with appropriate content type and attachment headers
    """
    
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id,
        user=request.user
    )
    
    # Use the utility function to format the conversation
    content, content_type, file_ext = format_conversation_for_download(conversation, format)
    
    # Create the response
    response = HttpResponse(content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="conversation_{conversation.id}.{file_ext}"'
    
    return response

# Favorite prompts views
@login_required
def favorite_prompts(request: HttpRequest, ai_id: Optional[int] = None) -> HttpResponse:
    """
    View and manage favorite prompts.
    
    This function displays the user's favorite prompts, optionally filtered by AI tool.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session
        ai_id (Optional[int]): ID of the AI tool to filter prompts by
        
    Returns:
        HttpResponse: Rendered template with the user's favorite prompts
    """
    
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
def save_favorite_prompt(request: HttpRequest) -> JsonResponse:
    """
    Save a prompt as favorite.
    
    This function processes a request to save a prompt as a favorite for the current user.
    
    Args:
        request (HttpRequest): The HTTP request object containing prompt data in JSON format
        
    Returns:
        JsonResponse: JSON indicating success or error information
    """
    
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
def delete_favorite_prompt(request: HttpRequest, prompt_id: int) -> HttpResponse:
    """
    Delete a favorite prompt.
    
    This function handles the deletion of a favorite prompt, with confirmation page.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session
        prompt_id (int): ID of the prompt to delete
        
    Returns:
        HttpResponse: Redirect to favorite prompts on successful deletion,
                     or confirmation page on GET request
    """
    
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
def share_conversation(request: HttpRequest, conversation_id: str) -> HttpResponse:
    """
    Share a conversation with others.
    
    This function handles the sharing of a conversation, either publicly or with a specific user.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session and form data
        conversation_id (str): UUID of the conversation to share
        
    Returns:
        HttpResponse: Rendered template with sharing success information or sharing form
    """
    
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

def view_shared_chat(request: HttpRequest, access_token: str) -> HttpResponse:
    """
    View a shared conversation.
    
    This function displays a shared conversation if the user has access to it.
    
    Args:
        request (HttpRequest): The HTTP request object containing user session
        access_token (str): Access token for the shared conversation
        
    Returns:
        HttpResponse: Rendered template with the shared conversation or access denied page
    """
    
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

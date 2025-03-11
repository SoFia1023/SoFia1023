from .models import AITool
from interaction.models import Conversation, Message, UserFavorite
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import json
import time
from typing import Dict, Any, List, Optional, Union, Type, TypeVar, cast
from django.db.models.query import QuerySet
from . import utils
from .mixins import PaginationMixin

# Define categories for AI tools
CATEGORIES = [
    'Text Generator',
    'Image Generator',
    'Video Generator',
    'Code Generator',
    'Transcription',
    'Word Processor',
    'AI Platform'
]

User = get_user_model()


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page with a showcase of top AI tools.
    
    This view displays the landing page of the application, featuring the most popular
    AI tools to attract user interest.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered home page with popular AI tools context
    """
    # Get 3 most popular AIs to showcase
    popular_ais = AITool.objects.all().order_by('-popularity')[:3]
    return render(request, 'catalog/home.html', {
        'popular_ais': popular_ais
    })


class AIToolDetailView(DetailView):
    """
    Display detailed information about a specific AI tool.
    
    This view provides detailed information about an AI tool, including its description,
    provider, category, and related tools in the same category.
    
    Attributes:
        model (Model): The model class this view displays
        template_name (str): The template used for rendering
        context_object_name (str): The variable name for the object in the template
        pk_url_kwarg (str): The URL parameter name for the primary key
    """
    model = AITool
    template_name = 'catalog/presentationAI.html'
    context_object_name = 'ai_tool'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add related AI tools to the context.
        
        This method enhances the template context with related AI tools in the same category
        and the favorite status for authenticated users.
        
        Args:
            **kwargs: Additional keyword arguments
            
        Returns:
            Dict[str, Any]: The enhanced context dictionary
        """
        context = super().get_context_data(**kwargs)
        
        # Get related AIs in the same category (limited to 3)
        ai_tool = self.get_object()
        related_ais = AITool.objects.filter(
            category=ai_tool.category
        ).exclude(id=ai_tool.id).order_by('-popularity')[:3]
        
        context['related_ais'] = related_ais
        
        # Add favorite status if user is authenticated
        if self.request.user.is_authenticated:
            context['is_favorite'] = UserFavorite.objects.filter(
                user=self.request.user,
                ai_tool=ai_tool
            ).exists()
        
        return context


# Available categories for AI tools
CATEGORIES = ["Text Generator", "Image Generator", "Video Generator", "Transcription", "Word Processor", "Code Generator", "AI Platform"]

class CatalogView(PaginationMixin, ListView):
    """
    Display the catalog of AI tools with filtering, sorting, and search capabilities.
    
    This view presents AI tools in a catalog format with advanced filtering options,
    search functionality, and sorting capabilities. It uses the OpenRouter-inspired
    design from models.html template.
    
    Attributes:
        model (Model): The model class this view displays
        template_name (str): The template used for rendering
        context_object_name (str): The variable name for the object list in the template
        paginate_by (int): Number of items to display per page
    """
    model = AITool
    template_name = 'catalog/models.html'  # Using the new models.html template
    context_object_name = 'ai_tools'
    paginate_by = 12  # Show 12 AI tools per page
    
    def get_queryset(self) -> QuerySet[AITool]:
        """
        Filter and sort the queryset based on request parameters.
        
        This method applies search filters, category filters, and sorting options
        to the AITool queryset based on GET parameters in the request.
        
        Returns:
            QuerySet[AITool]: Filtered and sorted queryset of AI tools
        """
        queryset = AITool.objects.all()
        
        # Apply search filter if provided
        search_query = self.request.GET.get('searchAITool', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(provider__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Apply category filter if provided
        category = self.request.GET.get('category', '')
        if category and category != 'All':
            queryset = queryset.filter(category=category)
        
        # Apply sorting if provided
        sort_by = self.request.GET.get('sort', 'popularity_desc')
        if sort_by == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort_by == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort_by == 'popularity_asc':
            queryset = queryset.order_by('popularity')
        elif sort_by == 'provider':
            queryset = queryset.order_by('provider')
        else:  # Default to popularity (highest first)
            queryset = queryset.order_by('-popularity')
        
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add additional context data for the template.
        
        This method enhances the template context with search parameters, filtering options,
        and user favorites for authenticated users.
        
        Args:
            **kwargs: Additional keyword arguments
            
        Returns:
            Dict[str, Any]: The enhanced context dictionary with filter parameters
        """
        context = super().get_context_data(**kwargs)
        
        # Add filter parameters to context for maintaining state
        context['searchTerm'] = self.request.GET.get('searchAITool', '')
        context['current_category'] = self.request.GET.get('category', 'All')
        context['sort'] = self.request.GET.get('sort', 'popularity')
        context['categories'] = CATEGORIES
        
        # Add user favorites if user is authenticated
        if self.request.user.is_authenticated:
            user_favorites = UserFavorite.objects.filter(
                user=self.request.user
            ).values_list('ai_tool_id', flat=True)
            context['user_favorites'] = user_favorites
        
        return context

# Keep the function-based view for backward compatibility
def catalog_view(request: HttpRequest) -> HttpResponse:
    """
    Legacy function-based view that redirects to the class-based view.
    
    This function exists for backward compatibility with code that might still
    reference the function-based view.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Response from the class-based view
    """
    return CatalogView.as_view()(request)


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration.
    
    This view processes user registration forms, validates the input data,
    creates new user accounts, and logs in the user upon successful registration.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Redirect to home page on success or registration form with errors
    """
    """Handle user registration."""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'catalog/register.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'catalog/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'catalog/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'catalog/register.html')
        
        # Create user
        User = get_user_model()
        # Type assertion to help mypy understand this is a UserManager with create_user
        user = cast(Any, User.objects).create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Log in the user
        login(request, user)
        messages.success(request, 'Registration successful! Welcome to InspireAI.')
        
        return redirect('home')
    
    return render(request, 'catalog/register.html')


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user login.
    
    This view authenticates users based on username and password,
    manages session expiration based on the 'remember me' option,
    and redirects to the appropriate page after login.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Redirect to next page on success or login form with errors
    """
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if not remember:
                # Session expires when browser closes
                request.session.set_expiry(0)
            messages.success(request, f'Welcome back, {username}!')
            
            # Redirect to the page the user was trying to access, or home
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'catalog/login.html')


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user logout.
    
    This view logs out the current user, terminates their session,
    and redirects them to the home page with a success message.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Redirect to home page after logout
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    Display user profile with favorite AI tools and activity.
    
    This view shows the user's profile information, their favorite AI tools,
    and their recent conversation history.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered profile page with user data context
    """
    # Get user's favorite AI tools
    favorites = UserFavorite.objects.filter(user=request.user).select_related('ai_tool')
    
    # Get user's recent conversations
    recent_conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')[:5]
    
    return render(request, 'catalog/profile.html', {
        'user': request.user,
        'favorites': favorites,
        'recent_conversations': recent_conversations
    })


# Chat view moved to interaction app


# Send message function moved to interaction app


# Download conversation function moved to interaction app


@login_required
@require_POST
def toggle_favorite(request: HttpRequest, ai_id: str) -> JsonResponse:
    """
    Toggle favorite status for an AI tool.
    
    This view adds or removes an AI tool from a user's favorites list
    and returns a JSON response indicating the new status.
    
    Args:
        request (HttpRequest): The HTTP request object
        ai_id (str): UUID of the AI tool to toggle
        
    Returns:
        JsonResponse: JSON response with success status and message
    """
    ai_tool = get_object_or_404(AITool, id=ai_id)
    
    # Check if already favorited
    favorite, created = UserFavorite.objects.get_or_create(user=request.user, ai_tool=ai_tool)
    
    if not created:
        # If it existed, delete it (unfavorite)
        favorite.delete()
        status = 'removed'
    else:
        # If it was created, it's now favorited
        status = 'added'
    
    # Return JSON response
    return JsonResponse({
        'success': True,
        'status': status,
        'message': f"AI tool {status} {'to' if status == 'added' else 'from'} favorites"
    })


# Chat selection view moved to interaction app


def compare_tools(request: HttpRequest) -> HttpResponse:
    """
    Compare two AI tools side by side.
    
    This view allows users to compare features and capabilities of two AI tools
    by displaying them in a side-by-side comparison layout.
    
    Args:
        request (HttpRequest): The HTTP request object containing tool IDs to compare
        
    Returns:
        HttpResponse: Rendered comparison page with tool data
    """
    tool1_id = request.GET.get('tool1')
    tool2_id = request.GET.get('tool2')
    
    tool1 = None
    tool2 = None
    
    if tool1_id:
        try:
            tool1 = AITool.objects.get(id=tool1_id)
        except AITool.DoesNotExist:
            pass
    
    if tool2_id:
        try:
            tool2 = AITool.objects.get(id=tool2_id)
        except AITool.DoesNotExist:
            pass
    
    # Get all AI tools for the dropdowns
    all_tools = AITool.objects.all().order_by('name')
    
    return render(request, 'catalog/compare.html', {
        'tool1': tool1,
        'tool2': tool2,
        'all_tools': all_tools
    })

# Keep the function-based view for backward compatibility
def presentationAI(request: HttpRequest, id: str) -> HttpResponse:
    """
    Legacy function-based view that redirects to the class-based view.
    
    This function exists for backward compatibility with code that might still
    reference the function-based view for AI tool details.
    
    Args:
        request (HttpRequest): The HTTP request object
        id (str): UUID of the AI tool to display
        
    Returns:
        HttpResponse: Response from the class-based view
    """
    return AIToolDetailView.as_view()(request, id=id)


class ModelsView(PaginationMixin, ListView):
    """
    Display AI models in a grid layout with filtering and search capabilities.
    
    This view presents AI tools in a modern grid layout with filtering options,
    search functionality, and sorting capabilities. The design is inspired by
    OpenRouter's models page.
    
    Attributes:
        model (Model): The model class this view displays
        template_name (str): The template used for rendering
        context_object_name (str): The variable name for the object list in the template
        paginate_by (int): Number of items to display per page
    """
    model = AITool
    template_name = 'catalog/models.html'
    context_object_name = 'ai_tools'
    paginate_by = 12  # Show 12 AI tools per page
    
    def get_queryset(self) -> QuerySet[AITool]:
        """
        Filter and sort the queryset based on request parameters.
        
        This method applies search filters, category filters, and sorting options
        to the AITool queryset based on GET parameters in the request.
        
        Returns:
            QuerySet[AITool]: Filtered and sorted queryset of AI tools
        """
        queryset = AITool.objects.all()
        
        # Apply search filter if provided
        search_query = self.request.GET.get('searchAITool', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(provider__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Apply category filter if provided
        category = self.request.GET.get('category', '')
        if category and category != 'All':
            queryset = queryset.filter(category=category)
        
        # Apply sorting if provided
        sort_by = self.request.GET.get('sort', 'popularity_desc')
        if sort_by == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort_by == 'name_desc':
            queryset = queryset.order_by('-name')
        elif sort_by == 'popularity_asc':
            queryset = queryset.order_by('popularity')
        elif sort_by == 'provider':
            queryset = queryset.order_by('provider')
        else:  # Default to popularity (highest first)
            queryset = queryset.order_by('-popularity')
        
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add additional context data for the template.
        
        This method enhances the template context with search parameters, filtering options,
        and user favorites for authenticated users.
        
        Args:
            **kwargs: Additional keyword arguments
            
        Returns:
            Dict[str, Any]: The enhanced context dictionary with filter parameters
        """
        context = super().get_context_data(**kwargs)
        
        # Add filter parameters to context for maintaining state
        context['searchTerm'] = self.request.GET.get('searchAITool', '')
        context['current_category'] = self.request.GET.get('category', 'All')
        context['sort'] = self.request.GET.get('sort', 'popularity')
        context['categories'] = CATEGORIES
        
        # Add user favorites if user is authenticated
        if self.request.user.is_authenticated:
            user_favorites = UserFavorite.objects.filter(
                user=self.request.user
            ).values_list('ai_tool_id', flat=True)
            context['user_favorites'] = user_favorites
        
        return context


# Function-based view for models page for backward compatibility
def models_view(request: HttpRequest) -> HttpResponse:
    """
    Legacy function-based view that redirects to the class-based view.
    
    This function exists for backward compatibility with code that might still
    reference the function-based view for the models page.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Response from the class-based view
    """
    return ModelsView.as_view()(request)
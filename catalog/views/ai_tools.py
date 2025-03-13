"""
AI Tools views for the catalog app.

This module contains views related to AI tool details and comparisons.
"""
import uuid
from typing import Any, Dict, List, Optional
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import DetailView

from catalog.models import AITool,Rating
from catalog.forms import RatingForm
from django.contrib import messages
from django.urls import reverse

# Using CustomUser.favorites directly


class AIToolDetailView(DetailView):
    """
    View for displaying the details of an AI tool.
    
    This view renders a detailed page for a specific AI tool.
    """
    model = AITool
    template_name = 'catalog/ai_tool_detail.html'
    context_object_name = 'ai_tool'
    pk_url_kwarg = 'id'  # Match the URL pattern parameter name
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Get the context data for the template.
        
        Args:
            **kwargs: Additional keyword arguments
            
        Returns:
            Context data dictionary
        """
        context = super().get_context_data(**kwargs)
        
        # Check if the user has favorited this AI tool
        if self.request.user.is_authenticated:
            context['is_favorite'] = self.request.user.favorites.filter(id=self.object.id).exists()
        else:
            context['is_favorite'] = False
        
        # Get related AI tools in the same category
        context['related_tools'] = AITool.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        
        return context


def presentationAI(request: HttpRequest, id: uuid.UUID) -> HttpResponse:
    """
    View for displaying a presentation-style page for an AI tool.

    This view renders a presentation-style page for a specific AI tool,
    allowing users to rate it, mark it as a favorite, and view related tools.

    Args:
        request: The HTTP request object.
        id: The UUID of the AI tool.

    Returns:
        Rendered presentation page.
    """
    # Get AI and related tools
    ai_tool = get_object_or_404(AITool, id=id)
    related_tools = AITool.objects.filter(category=ai_tool.category).exclude(id=ai_tool.id)[:4]
    
    # Check if the user has it in favorites
    is_favorite = request.user.is_authenticated and request.user.favorites.filter(id=ai_tool.id).exists()

    # Get ratings and star ratings
    ratings = ai_tool.ratings.all()
    average_rating = ai_tool.get_average_rating()

    # Manage rating submission
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                user=request.user, ai_tool=ai_tool,
                defaults={'stars': form.cleaned_data['stars'], 'comment': form.cleaned_data['comment']}
            )
             # Recalcular el promedio después de guardar la calificación 
            ai_tool.refresh_from_db()
            average_rating = ai_tool.get_average_rating()

            # Add a success message
            messages.success(request, '¡Rating saved successfully!')
        else:
            # Add an error message if the form is invalid
            messages.error(request, 'There was a problem saving the rating.')

    else:
        form = RatingForm()

    return render(request, 'catalog/PresentationAI.html', {
        'ai_tool': ai_tool,
        'is_favorite': is_favorite,
        'related_tools': related_tools,
        'ratings': ratings,
        'average_rating': average_rating,
        'form': form
    })




def compare_tools(request: HttpRequest) -> HttpResponse:
    """
    View for comparing multiple AI tools.
    
    This view renders a comparison page for multiple AI tools,
    allowing users to compare features and capabilities.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered comparison page
    """
    # Get the tool IDs from the request
    tool_ids = request.GET.getlist('tool_id')
    
    # Get the AI tools
    tools = []
    if tool_ids:
        tools = AITool.objects.filter(id__in=tool_ids)
    
    # If no tools are selected, show a selection page
    if not tools:
        # Get all AI tools for selection
        all_tools = AITool.objects.all().order_by('category', 'name')
        
        return render(request, 'catalog/compare_select.html', {
            'all_tools': all_tools
        })
    
    # Organize features for comparison
    features = [
        'name', 'provider', 'category', 'popularity', 'api_type',
        'api_model', 'is_featured'
    ]
    
    # Create a comparison table
    comparison = {}
    for feature in features:
        # Use a try-except block to handle missing attributes gracefully
        feature_values = []
        for tool in tools:
            try:
                feature_values.append(getattr(tool, feature))
            except AttributeError:
                # If the attribute doesn't exist, use a placeholder value
                feature_values.append('N/A')
        comparison[feature] = feature_values
    
    return render(request, 'catalog/compare.html', {
        'tools': tools,
        'features': features,
        'comparison': comparison
    })

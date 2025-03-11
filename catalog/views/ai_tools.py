"""
AI Tools views for the catalog app.

This module contains views related to AI tool details and comparisons.
"""
from typing import Any, Dict, List, Optional
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from catalog.models import AITool
# Using CustomUser.favorites directly


class AIToolDetailView(DetailView):
    """
    View for displaying the details of an AI tool.
    
    This view renders a detailed page for a specific AI tool.
    """
    model = AITool
    template_name = 'catalog/ai_tool_detail.html'
    context_object_name = 'ai_tool'
    
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


def presentationAI(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View for displaying a presentation-style page for an AI tool.
    
    This view renders a presentation-style page for a specific AI tool,
    focusing on its features and capabilities.
    
    Args:
        request: The HTTP request object
        pk: The primary key of the AI tool
        
    Returns:
        Rendered presentation page
    """
    # Get the AI tool
    ai_tool = get_object_or_404(AITool, pk=pk)
    
    # Check if the user has favorited this AI tool
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = request.user.favorites.filter(id=ai_tool.id).exists()
    
    # Get related AI tools in the same category
    related_tools = AITool.objects.filter(
        category=ai_tool.category
    ).exclude(id=ai_tool.id)[:4]
    
    return render(request, 'catalog/presentation.html', {
        'ai_tool': ai_tool,
        'is_favorite': is_favorite,
        'related_tools': related_tools
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
        'name', 'provider', 'category', 'is_free', 'pricing_model',
        'has_api', 'popularity'
    ]
    
    # Create a comparison table
    comparison = {}
    for feature in features:
        comparison[feature] = [getattr(tool, feature) for tool in tools]
    
    return render(request, 'catalog/compare.html', {
        'tools': tools,
        'features': features,
        'comparison': comparison
    })

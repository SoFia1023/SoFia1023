"""
Catalog views for the catalog app.

This module contains views related to browsing and filtering the catalog of AI tools.
"""
from typing import Any, Dict, List, Optional
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from catalog.models import AITool
from core.mixins import PaginationMixin, FilterMixin


class CatalogView(PaginationMixin, FilterMixin, ListView):
    """
    View for displaying the catalog of AI tools with filtering and pagination.
    
    This view renders a list of AI tools with various filtering options and pagination.
    """
    model = AITool
    template_name = 'catalog/catalog.html'
    context_object_name = 'ai_tools'
    paginate_by = 12
    
    def get_queryset(self) -> Any:
        """
        Get the queryset with applied filters.
        
        Returns:
            Filtered queryset of AI tools
        """
        queryset = super().get_queryset()
        
        # Apply search filter
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(provider__icontains=search_query)
            )
            
        # Apply category filter
        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
            
        # Apply pricing filter
        pricing = self.request.GET.get('pricing', None)
        if pricing == 'free':
            queryset = queryset.filter(is_free=True)
        elif pricing == 'paid':
            queryset = queryset.filter(is_free=False)
            
        # Apply sorting
        sort_by = self.request.GET.get('sort', 'popularity')
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'popularity':
            queryset = queryset.order_by('-popularity')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
            
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Get the context data for the template.
        
        Args:
            **kwargs: Additional keyword arguments
            
        Returns:
            Context data dictionary
        """
        context = super().get_context_data(**kwargs)
        
        # Add filter parameters to context
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_pricing'] = self.request.GET.get('pricing', '')
        context['sort_by'] = self.request.GET.get('sort', 'popularity')
        
        # Add categories for filter dropdown
        categories = AITool.objects.values_list('category', flat=True).distinct()
        context['categories'] = [cat for cat in categories if cat]
        
        # Add pagination context
        context = self.get_pagination_context(context)
        
        return context


def catalog_view(request: HttpRequest) -> HttpResponse:
    """
    Function-based view for the catalog page.
    
    This is a simpler alternative to the class-based CatalogView.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered catalog page
    """
    # Get filter parameters from request
    search_query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    pricing = request.GET.get('pricing', '')
    sort_by = request.GET.get('sort', 'popularity')
    
    # Start with all AI tools
    queryset = AITool.objects.all()
    
    # Apply search filter
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(provider__icontains=search_query)
        )
        
    # Apply category filter
    if category:
        queryset = queryset.filter(category=category)
        
    # Apply pricing filter
    if pricing == 'free':
        queryset = queryset.filter(is_free=True)
    elif pricing == 'paid':
        queryset = queryset.filter(is_free=False)
        
    # Apply sorting
    if sort_by == 'name':
        queryset = queryset.order_by('name')
    elif sort_by == 'popularity':
        queryset = queryset.order_by('-popularity')
    elif sort_by == 'newest':
        queryset = queryset.order_by('-created_at')
    
    # Get categories for filter dropdown
    categories = AITool.objects.values_list('category', flat=True).distinct()
    categories = [cat for cat in categories if cat]
    
    return render(request, 'catalog/catalog.html', {
        'ai_tools': queryset,
        'search_query': search_query,
        'selected_category': category,
        'selected_pricing': pricing,
        'sort_by': sort_by,
        'categories': categories
    })


class ModelsView(PaginationMixin, ListView):
    """
    View for displaying AI models with pagination.
    
    This view renders a list of AI models, which are a subset of AI tools.
    """
    model = AITool
    template_name = 'catalog/models.html'
    context_object_name = 'ai_models'
    paginate_by = 12
    
    def get_queryset(self) -> Any:
        """
        Get the queryset of AI models.
        
        Returns:
            Filtered queryset of AI models
        """
        # Filter to only include AI models
        return AITool.objects.filter(category='Model').order_by('-popularity')
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Get the context data for the template.
        
        Args:
            **kwargs: Additional keyword arguments
            
        Returns:
            Context data dictionary
        """
        context = super().get_context_data(**kwargs)
        
        # Add pagination context
        context = self.get_pagination_context(context)
        
        return context


def models_view(request: HttpRequest) -> HttpResponse:
    """
    Function-based view for the models page.
    
    This is a simpler alternative to the class-based ModelsView.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered models page
    """
    # Get AI models
    ai_models = AITool.objects.filter(category='Model').order_by('-popularity')
    
    return render(request, 'catalog/models.html', {
        'ai_models': ai_models
    })

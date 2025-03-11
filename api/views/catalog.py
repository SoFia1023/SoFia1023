"""
API views for the catalog app.

This module contains API views for the catalog app, including viewsets and function-based views.
"""
from typing import Any, Dict, List, Optional, Union, cast
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request

from catalog.models import AITool


class AIToolViewSet(viewsets.ModelViewSet):
    """
    API endpoint for AI tools.
    
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = AITool.objects.all().order_by('name')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """
        Return different serializers for list and detail views.
        
        Returns:
            Serializer class appropriate for the request
        """
        from api.serializers.catalog import AIToolSerializer, AIToolDetailSerializer
        
        if self.action == 'retrieve':
            return AIToolDetailSerializer
        return AIToolSerializer
    
    def get_queryset(self) -> Any:
        """
        Filter queryset based on query parameters.
        
        Returns:
            Filtered queryset
        """
        queryset = super().get_queryset()
        
        # Apply search filter
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(provider__icontains=search_query)
            )
            
        # Apply category filter
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
            
        # Apply sorting
        sort_by = self.request.query_params.get('sort', None)
        if sort_by:
            if sort_by == 'name':
                queryset = queryset.order_by('name')
            elif sort_by == 'popularity':
                queryset = queryset.order_by('-popularity')
            elif sort_by == 'newest':
                queryset = queryset.order_by('-created_at')
                
        return queryset


@api_view(['GET'])
def search_ai_tools(request: Request) -> Response:
    """
    Search AI tools based on query parameters.
    
    Args:
        request: The request object containing search parameters
        
    Returns:
        Response with search results
    """
    query = request.query_params.get('q', '')
    category = request.query_params.get('category', '')
    
    # Start with all AI tools
    queryset = AITool.objects.all()
    
    # Apply search filter if query is provided
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(provider__icontains=query)
        )
        
    # Apply category filter if category is provided
    if category:
        queryset = queryset.filter(category=category)
        
    # Limit to 20 results for performance
    queryset = queryset[:20]
    
    # Convert to list of dictionaries
    results = []
    for tool in queryset:
        results.append({
            'id': str(tool.id),
            'name': tool.name,
            'description': tool.description,
            'provider': tool.provider,
            'category': tool.category,
            'logo_url': tool.logo_url if tool.logo_url else '',
        })
        
    return Response(results)


@api_view(['GET'])
def list_categories(request: Request) -> Response:
    """
    List all available AI tool categories.
    
    Args:
        request: The request object
        
    Returns:
        Response with list of categories
    """
    # Get distinct categories from the database
    categories = AITool.objects.values_list('category', flat=True).distinct()
    
    # Convert QuerySet to list and remove any None values
    category_list = [cat for cat in categories if cat]
    
    return Response(category_list)

"""
Core mixins for class-based views.

This module contains mixins that can be used across different apps
to provide common functionality to class-based views.
"""
from typing import Any, Dict, List, Optional, TypeVar, Union, cast
from django.db.models.query import QuerySet
from django.http import HttpRequest


class PaginationMixin:
    """
    Mixin for handling pagination in list views.
    
    This mixin provides methods for paginating querysets and adding
    pagination context to templates.
    """
    
    def get_pagination_context(self, context: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """
        Add pagination context to the template context.
        
        Args:
            context: The existing context dictionary
            **kwargs: Additional keyword arguments
            
        Returns:
            The updated context dictionary with pagination information
        """
        page_obj = context.get('page_obj')
        if not page_obj:
            return context
            
        # Add pagination range
        paginator = page_obj.paginator
        current_page = page_obj.number
        
        # Calculate page range to display (show 5 pages around current page)
        page_range_start = max(current_page - 2, 1)
        page_range_end = min(current_page + 2, paginator.num_pages)
        
        # Ensure we always show 5 pages if possible
        if page_range_end - page_range_start < 4 and paginator.num_pages > 4:
            if page_range_start == 1:
                page_range_end = min(5, paginator.num_pages)
            elif page_range_end == paginator.num_pages:
                page_range_start = max(paginator.num_pages - 4, 1)
                
        context['page_range'] = range(page_range_start, page_range_end + 1)
        context['show_first'] = page_range_start > 1
        context['show_last'] = page_range_end < paginator.num_pages
        
        return context


class FilterMixin:
    """
    Mixin for handling filtering in list views.
    
    This mixin provides methods for filtering querysets based on
    request parameters and adding filter context to templates.
    """
    
    def get_filter_params(self, request: HttpRequest) -> Dict[str, Any]:
        """
        Extract filter parameters from the request.
        
        Args:
            request: The HTTP request object
            
        Returns:
            Dictionary of filter parameters
        """
        params = {}
        
        # Extract query parameters
        query = request.GET.get('q', '')
        if query:
            params['q'] = query
            
        # Extract category filters
        category = request.GET.get('category', '')
        if category:
            params['category'] = category
            
        # Extract sort parameters
        sort = request.GET.get('sort', '')
        if sort:
            params['sort'] = sort
            
        return params
    
    def apply_filters(self, queryset: QuerySet, params: Dict[str, Any]) -> QuerySet:
        """
        Apply filters to the queryset based on parameters.
        
        Args:
            queryset: The base queryset to filter
            params: Dictionary of filter parameters
            
        Returns:
            Filtered queryset
        """
        # This is a base implementation that should be overridden
        # by subclasses to provide specific filtering logic
        return queryset
    
    def get_filter_context(self, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add filter context to the template context.
        
        Args:
            context: The existing context dictionary
            params: Dictionary of filter parameters
            
        Returns:
            The updated context dictionary with filter information
        """
        # Add filter parameters to context
        context.update(params)
        
        # Add query string for pagination links
        query_items = []
        for key, value in params.items():
            if key != 'page' and value:  # Exclude page from query string
                query_items.append(f"{key}={value}")
                
        context['query_string'] = '&'.join(query_items)
        
        return context


class UserFavoriteMixin:
    """
    Mixin for handling user favorites in views.
    
    This mixin provides methods for checking and adding user favorite
    information to the template context.
    """
    
    def get_user_favorites(self, user: Any) -> List[str]:
        """
        Get list of user's favorite item IDs.
        
        Args:
            user: The user object
            
        Returns:
            List of favorite item IDs as strings
        """
        if not user or not user.is_authenticated:
            return []
            
        # This is a base implementation that should be overridden
        # by subclasses to provide specific favorite retrieval logic
        return []
    
    def add_favorites_to_context(self, context: Dict[str, Any], user: Any) -> Dict[str, Any]:
        """
        Add user favorites information to the template context.
        
        Args:
            context: The existing context dictionary
            user: The user object
            
        Returns:
            The updated context dictionary with favorites information
        """
        if user and user.is_authenticated:
            context['user_favorites'] = self.get_user_favorites(user)
            
        return context

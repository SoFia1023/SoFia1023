from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest
from django.db.models.query import QuerySet
from typing import Any, Dict, List, Optional, Tuple, Union, cast

class PaginationMixin:
    """
    A mixin to add pagination functionality to class-based views.
    
    Attributes:
        paginate_by (int): Number of items per page
        page_kwarg (str): The name of the URL query parameter for the page number
    """
    paginate_by = 10
    page_kwarg = 'page'
    
    # These attributes are expected to be provided by the view that uses this mixin
    request: HttpRequest
    
    def get_queryset(self) -> QuerySet:
        # This method is expected to be implemented by the view that uses this mixin
        raise NotImplementedError("Subclasses must implement get_queryset()")
    
    def paginate_queryset(self, queryset: QuerySet, page_size: Optional[int] = None) -> Tuple[Paginator, Any, Any, bool]:
        """
        Paginate the queryset.
        
        Args:
            queryset: The queryset to paginate
            page_size (int, optional): Number of items per page. Defaults to self.paginate_by.
            
        Returns:
            tuple: (paginator, page, page_obj, is_paginated)
        """
        page_size = page_size or self.paginate_by
        paginator = Paginator(queryset, page_size)
        page_number = self.request.GET.get(self.page_kwarg, 1)
        
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            
        is_paginated = paginator.num_pages > 1
        return (paginator, page, page.object_list, is_paginated)
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Add pagination context data.
        
        Returns:
            dict: Context data with pagination information
        """
        # Using Any for the parent class since we don't know what it is
        # This is a mixin that can be used with different view types
        context = super().get_context_data(**kwargs)  # type: ignore
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset)
        
        context.update({
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            'object_list': queryset
        })
        
        # Add page range for better navigation
        if is_paginated:
            # Show 3 pages before and after the current page
            current_page = page.number
            total_pages = paginator.num_pages
            
            # Calculate the range of pages to display
            start_page = max(current_page - 3, 1)
            end_page = min(current_page + 3, total_pages)
            
            # Create the page range
            page_range = range(start_page, end_page + 1)
            context['page_range'] = page_range
            
        return context 
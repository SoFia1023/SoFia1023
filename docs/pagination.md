# Pagination Implementation Guide

This document outlines the standardized approach to pagination across the InspireIA application.

## Overview

Pagination is implemented consistently across all list views in the application using Django's built-in pagination functionality. This ensures a uniform user experience and optimizes performance by limiting the number of items displayed per page.

## Implementation Details

### Core Components

1. **PaginationMixin**: A reusable mixin in `core/mixins.py` that provides pagination functionality for class-based views.
2. **Pagination Template**: A reusable template partial in `core/templates/core/partials/pagination.html` that renders the pagination UI.
3. **Function-Based View Implementation**: Standard pagination implementation for function-based views.

### Class-Based Views

For class-based views, use the `PaginationMixin` along with Django's `ListView`:

```python
from django.views.generic import ListView
from core.mixins import PaginationMixin

class MyListView(PaginationMixin, ListView):
    model = MyModel
    template_name = 'my_template.html'
    context_object_name = 'items'
    paginate_by = 10  # Number of items per page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add pagination context
        context = self.get_pagination_context(context)
        return context
```

### Function-Based Views

For function-based views, use Django's `Paginator` class:

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def my_list_view(request):
    items_list = MyModel.objects.all().order_by('-created_at')
    
    # Paginate the items list
    paginator = Paginator(items_list, 10)  # Show 10 items per page
    page = request.GET.get('page', 1)
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        items = paginator.page(paginator.num_pages)
    
    # Calculate page range to display (show 5 pages around current page)
    current_page = items.number
    page_range_start = max(current_page - 2, 1)
    page_range_end = min(current_page + 2, paginator.num_pages)
    
    # Ensure we always show 5 pages if possible
    if page_range_end - page_range_start < 4 and paginator.num_pages > 4:
        if page_range_start == 1:
            page_range_end = min(5, paginator.num_pages)
        elif page_range_end == paginator.num_pages:
            page_range_start = max(paginator.num_pages - 4, 1)
    
    return render(request, 'my_template.html', {
        'items': items,
        'page_obj': items,  # For consistent template access
        'paginator': paginator,
        'page_range': range(page_range_start, page_range_end + 1),
        'show_first': page_range_start > 1,
        'show_last': page_range_end < paginator.num_pages
    })
```

### Template Implementation

Include the pagination component in your template:

```html
{% include 'core/partials/pagination.html' %}
```

## Pagination Configuration

### Default Settings

- **Items per page**: 
  - 10 for conversation and shared chat lists
  - 12 for catalog and favorite prompts

### Customizing Items Per Page

To customize the number of items per page:

- For class-based views: Set the `paginate_by` attribute
- For function-based views: Adjust the second parameter in the `Paginator` constructor

## Best Practices

1. **Consistent Context Variables**: Always use the same context variable names for pagination:
   - `page_obj`: The current page object
   - `paginator`: The paginator instance
   - `page_range`: The range of page numbers to display
   - `show_first`: Boolean indicating whether to show a link to the first page
   - `show_last`: Boolean indicating whether to show a link to the last page

2. **URL Parameter Preservation**: The pagination component preserves all other URL parameters when navigating between pages.

3. **Accessibility**: The pagination component includes proper ARIA attributes and screen reader support.

4. **Responsive Design**: The pagination component is designed to work well on all screen sizes.

## Views with Pagination

The following views in the application implement pagination:

1. **Catalog Views**:
   - `CatalogView` (class-based)
   - `ModelsView` (class-based)

2. **Interaction Views**:
   - `conversation_history` (function-based)
   - `favorite_prompts` (function-based)
   - `manage_shared_chats` (function-based)

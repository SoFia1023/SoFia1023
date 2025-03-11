"""
Utility functions for Django admin classes with proper type annotations.
"""
from typing import Any, Callable, TypeVar, Optional, cast

F = TypeVar('F', bound=Callable[..., Any])

def admin_display(
    description: Optional[str] = None,
    boolean: Optional[bool] = None,
    ordering: Optional[str] = None,
    admin_order_field: Optional[str] = None,
    allow_tags: Optional[bool] = None,
    empty_value_display: Optional[str] = None,
) -> Callable[[F], F]:
    """
    A type-aware version of Django's admin display decorator.
    This helps mypy understand that admin display attributes are valid.
    
    Args:
        description: Short description for the admin
        boolean: Whether to display as a boolean
        ordering: Field to use for ordering
        admin_order_field: Field to use for ordering (alias for ordering)
        allow_tags: Whether to allow HTML tags
        empty_value_display: What to display when empty
        
    Returns:
        A decorator that preserves the function's type
    """
    def decorator(func: F) -> F:
        if description is not None:
            func.short_description = description  # type: ignore
        if boolean is not None:
            func.boolean = boolean  # type: ignore
        if ordering is not None:
            func.admin_order_field = ordering  # type: ignore
        if admin_order_field is not None:
            func.admin_order_field = admin_order_field  # type: ignore
        if allow_tags is not None:
            func.allow_tags = allow_tags  # type: ignore
        if empty_value_display is not None:
            func.empty_value_display = empty_value_display  # type: ignore
        return func
    return decorator

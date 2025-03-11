"""
Utility functions for type checking and annotations.
"""
from typing import Any, Callable, TypeVar, cast, Optional

T = TypeVar('T')

def admin_display(
    short_description: Optional[str] = None,
    boolean: Optional[bool] = None,
    ordering: Optional[str] = None,
    description: Optional[str] = None,
    empty_value_display: Optional[str] = None,
    admin_order_field: Optional[str] = None,
) -> Callable[[T], T]:
    """
    Decorator for Django admin display functions that preserves type information.
    This helps mypy understand that the decorated function maintains its original type.
    
    Args:
        short_description: A short description of the field for the admin
        boolean: Whether to display the field as a boolean
        ordering: The field to use for ordering
        description: A longer description of the field
        empty_value_display: What to display when the field is empty
        admin_order_field: The field to use for ordering
        
    Returns:
        The decorated function with admin display attributes
    """
    def decorator(func: T) -> T:
        if short_description is not None:
            func.short_description = short_description  # type: ignore
        if boolean is not None:
            func.boolean = boolean  # type: ignore
        if ordering is not None:
            func.ordering = ordering  # type: ignore
        if description is not None:
            func.description = description  # type: ignore
        if empty_value_display is not None:
            func.empty_value_display = empty_value_display  # type: ignore
        if admin_order_field is not None:
            func.admin_order_field = admin_order_field  # type: ignore
        return func
    return decorator

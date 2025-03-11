"""
Type stubs for Django admin classes to help mypy understand admin display attributes.
"""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, TypeVar, Union, Protocol

T = TypeVar('T')

class AdminDisplayCallable(Protocol):
    """Protocol for callables with admin display attributes."""
    short_description: str
    boolean: bool
    admin_order_field: str
    allow_tags: bool
    empty_value_display: str
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

def display(
    *, 
    description: Optional[str] = None,
    ordering: Optional[str] = None,
    boolean: Optional[bool] = None,
    empty_value_display: Optional[str] = None
) -> Callable[[T], T]: ...

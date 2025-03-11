from django import template
from typing import Any, Union, Optional, cast

register = template.Library()

@register.filter
def multiply(value: Any, arg: Any) -> float:
    """Multiplies the value by the argument
    
    Args:
        value: The value to multiply
        arg: The multiplier
        
    Returns:
        float: The result of multiplication or 0 if conversion fails
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0.0
        
@register.filter
def subtract(value: Any, arg: Any) -> int:
    """Subtracts the argument from the value
    
    Args:
        value: The base value
        arg: The value to subtract
        
    Returns:
        int: The result of subtraction or 0 if conversion fails
    """
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0
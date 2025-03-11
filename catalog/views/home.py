"""
Home view for the catalog app.

This module contains views related to the home page.
"""
from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from catalog.models import AITool


def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page with a showcase of top AI tools.
    
    This view displays the landing page of the application, featuring the most popular
    AI tools to attract user interest.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered home page with popular AI tools context
    """
    # Get 3 most popular AIs to showcase
    popular_ais = AITool.objects.all().order_by('-popularity')[:3]
    
    return render(request, 'catalog/home.html', {
        'popular_ais': popular_ais
    })

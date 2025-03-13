"""
Home view for the catalog app.

This module contains views related to the home page.
"""
from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.db.models import Avg
from catalog.models import AITool, Rating


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
    popular_ais = AITool.objects.annotate(
        average_rating=Avg('ratings__stars')
    ).order_by('-average_rating')[:6]
    
    context = {
        'popular_ais': popular_ais,
    }
    return render(request, 'catalog/home.html', context)

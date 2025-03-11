"""
Authentication views for the users app.

This module contains views related to user authentication, including registration, login, and logout.
"""
from typing import Any, Dict, Optional, Union
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from core.utils import get_client_ip
from users.forms import CustomUserCreationForm


@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:
    """
    View for user registration.
    
    This view handles user registration, displaying the registration form
    and processing form submissions.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered registration page or redirect to login
    """
    if request.user.is_authenticated:
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the registration
            ip_address = get_client_ip(request)
            # You could add logging here
            
            # Redirect to login page
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'users/register.html', {
        'form': form
    })


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    """
    View for user login.
    
    This view handles user login, displaying the login form
    and processing form submissions.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered login page or redirect to dashboard
    """
    if request.user.is_authenticated:
        return redirect('users:dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Log the login
                ip_address = get_client_ip(request)
                # You could add logging here
                
                # Redirect to dashboard or next page
                next_page = request.GET.get('next', 'users:dashboard')
                return redirect(next_page)
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {
        'form': form
    })


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    View for user logout.
    
    This view handles user logout, logging the user out and redirecting to the home page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Redirect to home
    """
    if request.user.is_authenticated:
        # Log the logout
        ip_address = get_client_ip(request)
        # You could add logging here
        
        # Logout the user
        logout(request)
        
    return redirect('catalog:home')

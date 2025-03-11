"""
Profile views for the users app.

This module contains views related to user profiles, including viewing and updating profiles.
"""
from typing import Any, Dict, Optional, Union
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from users.forms import UserProfileForm


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    View for displaying and updating the user's profile.
    
    This view renders the user's profile page and handles profile updates.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered profile page
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {
        'form': form
    })


@login_required
@require_http_methods(["GET", "POST"])
def update_profile(request: HttpRequest) -> HttpResponse:
    """
    View for updating the user's profile.
    
    This view handles updating the user's profile information.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered profile update page or redirect to profile
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/update_profile.html', {
        'form': form
    })


@login_required
@require_http_methods(["GET", "POST"])
def change_password(request: HttpRequest) -> HttpResponse:
    """
    View for changing the user's password.
    
    This view handles changing the user's password.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered password change page or redirect to profile
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {
        'form': form
    })

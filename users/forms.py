from typing import Dict, Any, List, Optional, Union, Type
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import FileExtensionValidator
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'username_exists': "This username is already taken.",
        'email_exists': "This email address is already in use.",
        'password_too_short': "Password must be at least 8 characters long.",
        'password_too_common': "Password is too common or easily guessable.",
        'password_entirely_numeric': "Password cannot be entirely numeric.",
    }
    
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        error_messages={
            'required': 'Email address is required.',
            'invalid': 'Please enter a valid email address.',
        }
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        error_messages={
            'required': 'Username is required.',
            'invalid': 'Please enter a valid username.',
            'max_length': 'Username is too long (maximum 150 characters).',
        },
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        error_messages={
            'required': 'First name is required.',
        }
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        error_messages={
            'required': 'Password is required.',
        },
        help_text="Password must be at least 8 characters and cannot be entirely numeric."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        error_messages={
            'required': 'Password confirmation is required.',
        },
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = CustomUser
        fields: List[str] = ['email', 'username', 'first_name', 'password1', 'password2']
        
    def clean_username(self) -> str:
        """
        Validate that the username is unique and properly formatted.
        
        Returns:
            The validated username
            
        Raises:
            forms.ValidationError: If the username is already in use or improperly formatted
        """
        username = self.cleaned_data.get('username')
        
        if username and CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['username_exists'], code='username_exists')
            
        # Check for valid characters
        if username and not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError(
                'Username may only contain letters, numbers, and @/./+/-/_ characters.',
                code='invalid_username'
            )
            
        return username
        
    def clean_email(self) -> str:
        """
        Validate that the email is unique and properly formatted.
        
        Returns:
            The validated email
            
        Raises:
            forms.ValidationError: If the email is already in use
        """
        email = self.cleaned_data.get('email')
        
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages['email_exists'], code='email_exists')
            
        return email


class CustomUserLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Please enter a correct username and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive. Please contact support for assistance.",
    }
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username",
        error_messages={
            'required': 'Username is required.',
            'invalid': 'Please enter a valid username.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password",
        error_messages={
            'required': 'Password is required.',
        }
    )
    
    def clean(self) -> Dict[str, Any]:
        """
        Override the default clean method to provide more specific error messages.
        
        Returns:
            The cleaned data dictionary
            
        Raises:
            forms.ValidationError: If authentication fails
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                # Check if the user exists but password is wrong
                if CustomUser.objects.filter(username=username).exists():
                    raise forms.ValidationError(
                        "The password you entered is incorrect. Please try again.",
                        code='incorrect_password'
                    )
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login'
                    )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive'
                )
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself', 'rows': 3}),
        max_length=500,
        help_text="Maximum 500 characters"
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],
        help_text="Supported formats: JPG, JPEG, PNG, GIF. Max size: 5MB"
    )
    
    class Meta:
        model = CustomUser
        fields: List[str] = ['email', 'first_name', 'last_name', 'bio', 'profile_picture']
        
    def clean_email(self) -> str:
        """
        Validate that the email is unique and properly formatted.
        
        Returns:
            The validated email
            
        Raises:
            forms.ValidationError: If the email is already in use by another user or improperly formatted
        """
        email = self.cleaned_data.get('email')
        username = self.instance.username
        
        if email and CustomUser.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email is already in use by another user.')
        
        # Additional validation for email format
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if email and not email_pattern.match(email):
            raise forms.ValidationError('Please enter a valid email address.')
            
        return email
    
    def clean_first_name(self) -> str:
        """
        Validate that the first name contains only letters and spaces.
        
        Returns:
            The validated first name
            
        Raises:
            forms.ValidationError: If the first name contains invalid characters
        """
        first_name = self.cleaned_data.get('first_name')
        
        if first_name and not all(c.isalpha() or c.isspace() for c in first_name):
            raise forms.ValidationError('First name should contain only letters and spaces.')
            
        return first_name
    
    def clean_last_name(self) -> str:
        """
        Validate that the last name contains only letters and spaces.
        
        Returns:
            The validated last name
            
        Raises:
            forms.ValidationError: If the last name contains invalid characters
        """
        last_name = self.cleaned_data.get('last_name')
        
        if last_name and not all(c.isalpha() or c.isspace() for c in last_name):
            raise forms.ValidationError('Last name should contain only letters and spaces.')
            
        return last_name
    
    def clean_profile_picture(self) -> Optional[Any]:
        """
        Validate that the profile picture is not too large.
        
        Returns:
            The validated profile picture
            
        Raises:
            forms.ValidationError: If the profile picture is too large
        """
        profile_picture = self.cleaned_data.get('profile_picture')
        
        if profile_picture:
            # Check file size (5MB limit)
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise forms.ValidationError('Profile picture size should not exceed 5MB.')
                
        return profile_picture

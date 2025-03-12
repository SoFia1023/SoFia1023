"""
Forms for the interaction app.

This module contains forms for creating and managing conversations, messages, and favorite prompts.
"""
from typing import Dict, Any, List, Optional, Union, Type, Set
import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Conversation, Message, FavoritePrompt, SharedChat
from catalog.models import AITool


class ConversationForm(forms.ModelForm):
    """
    Form for creating and updating conversations.
    """
    title = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Conversation Title'}),
        error_messages={
            'required': 'Please provide a title for this conversation.',
            'max_length': 'Title must be less than 255 characters.'
        }
    )
    
    class Meta:
        model = Conversation
        fields: List[str] = ['title', 'ai_tool']
        widgets = {
            'ai_tool': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'ai_tool': {
                'required': 'Please select an AI tool for this conversation.',
            }
        }
    
    def clean_title(self) -> str:
        """
        Validate that the conversation title is appropriate.
        
        Returns:
            The validated title
            
        Raises:
            forms.ValidationError: If the title contains inappropriate content
        """
        title = self.cleaned_data.get('title')
        
        # Check for minimum length
        if title and len(title.strip()) < 3:
            raise forms.ValidationError(
                'Conversation title must be at least 3 characters long.',
                code='title_too_short'
            )
        
        # Check for inappropriate content (simplified example)
        inappropriate_terms = ['spam', 'offensive', 'inappropriate']
        if title and any(term in title.lower() for term in inappropriate_terms):
            raise forms.ValidationError(
                'Conversation title contains inappropriate content.',
                code='inappropriate_title'
            )
        
        return title


class MessageForm(forms.ModelForm):
    """
    Form for creating and sending messages in a conversation.
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control message-input',
            'placeholder': 'Type your message here...',
            'rows': 3,
            'autofocus': True
        }),
        error_messages={
            'required': 'Message content cannot be empty.',
        }
    )
    
    class Meta:
        model = Message
        fields: List[str] = ['content']
    
    def clean_content(self) -> str:
        """
        Validate that the message content is appropriate and not empty.
        
        Returns:
            The validated content
            
        Raises:
            forms.ValidationError: If the content is empty or inappropriate
        """
        content = self.cleaned_data.get('content')
        
        # Check if content is empty or just whitespace
        if not content or not content.strip():
            raise forms.ValidationError(
                'Message content cannot be empty.',
                code='empty_content'
            )
        
        # Check for maximum length (e.g., 5000 characters)
        if len(content) > 5000:
            raise forms.ValidationError(
                'Message is too long. Please limit your message to 5000 characters.',
                code='content_too_long'
            )
        
        return content


class FavoritePromptForm(forms.ModelForm):
    """
    Form for creating and updating favorite prompts.
    """
    title = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prompt Title'}),
        error_messages={
            'required': 'Please provide a title for this prompt.',
            'max_length': 'Title must be less than 255 characters.'
        }
    )
    prompt_text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your prompt text here...',
            'rows': 5
        }),
        error_messages={
            'required': 'Prompt text cannot be empty.',
        }
    )
    ai_tools = forms.ModelMultipleChoiceField(
        queryset=AITool.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        help_text="Select the AI tools this prompt can be used with. Leave empty to use with all tools."
    )
    
    class Meta:
        model = FavoritePrompt
        fields: List[str] = ['title', 'prompt_text', 'ai_tools']
    
    def clean_title(self) -> str:
        """
        Validate that the prompt title is appropriate and unique for the user.
        
        Returns:
            The validated title
            
        Raises:
            forms.ValidationError: If the title is inappropriate or already exists
        """
        title = self.cleaned_data.get('title')
        user = self.instance.user if self.instance and hasattr(self.instance, 'user') else None
        
        # Check for minimum length
        if title and len(title.strip()) < 3:
            raise forms.ValidationError(
                'Prompt title must be at least 3 characters long.',
                code='title_too_short'
            )
        
        # Check for uniqueness for this user
        if user and title:
            # Exclude the current instance when checking for duplicates
            existing_prompts = FavoritePrompt.objects.filter(user=user, title=title)
            if self.instance and self.instance.pk:
                existing_prompts = existing_prompts.exclude(pk=self.instance.pk)
            
            if existing_prompts.exists():
                raise forms.ValidationError(
                    'You already have a prompt with this title. Please choose a different title.',
                    code='duplicate_title'
                )
        
        return title
    
    def clean_prompt_text(self) -> str:
        """
        Validate that the prompt text is appropriate and not empty.
        
        Returns:
            The validated prompt text
            
        Raises:
            forms.ValidationError: If the prompt text is empty or inappropriate
        """
        prompt_text = self.cleaned_data.get('prompt_text')
        
        # Check if prompt_text is empty or just whitespace
        if not prompt_text or not prompt_text.strip():
            raise forms.ValidationError(
                'Prompt text cannot be empty.',
                code='empty_prompt'
            )
        
        # Check for minimum length
        if len(prompt_text.strip()) < 10:
            raise forms.ValidationError(
                'Prompt text should be at least 10 characters long to be useful.',
                code='prompt_too_short'
            )
        
        # Check for maximum length
        if len(prompt_text) > 2000:
            raise forms.ValidationError(
                'Prompt text is too long. Please limit your prompt to 2000 characters.',
                code='prompt_too_long'
            )
        
        return prompt_text


class SharedChatForm(forms.ModelForm):
    """
    Form for sharing conversations with other users or publicly.
    """
    is_public = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Make this share public (anyone with the link can view)',
        help_text='If unchecked, only the selected recipient can view this conversation.'
    )
    
    recipient = forms.ModelChoiceField(
        queryset=None,  # Set in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        label='Share with specific user',
        help_text='Select a user to share this conversation with. Only required if not public.'
    )
    
    expiration_days = forms.IntegerField(
        required=True,
        min_value=0,
        max_value=365,
        initial=7,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Number of days until the shared chat expires. Use 0 for no expiration.",
        error_messages={
            'required': 'Please specify an expiration period.',
            'min_value': 'Expiration cannot be negative.',
            'max_value': 'Expiration cannot exceed 365 days.',
        }
    )
    
    class Meta:
        model = SharedChat
        fields: List[str] = ['is_public', 'recipient', 'expiration_days']
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the form with dynamic recipient queryset.
        """
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['recipient'].queryset = User.objects.all().order_by('username')
    
    def clean(self) -> Dict[str, Any]:
        """
        Validate that either is_public is True or a recipient is selected.
        
        Returns:
            The cleaned data
            
        Raises:
            forms.ValidationError: If validation fails
        """
        cleaned_data = super().clean()
        is_public = cleaned_data.get('is_public')
        recipient = cleaned_data.get('recipient')
        
        if not is_public and not recipient:
            self.add_error(
                'recipient',
                forms.ValidationError(
                    'You must select a recipient when sharing privately.',
                    code='recipient_required'
                )
            )
        
        return cleaned_data

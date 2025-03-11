import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
import json
from typing import List, Dict, Any, Optional, Union
from django.db.models.query import QuerySet
from catalog.models import AITool

class Conversation(models.Model):
    """Model representing a conversation between a user and an AI tool."""
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='interaction_conversations'
    )
    ai_tool: models.ForeignKey = models.ForeignKey(
        AITool, 
        on_delete=models.CASCADE,
        related_name='interaction_conversations'
    )
    title: models.CharField = models.CharField(max_length=255, default="New Conversation")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        # Type checking: ensure user has username attribute
        user_str = self.user.username if self.user and hasattr(self.user, 'username') else "Anonymous"
        # Type checking: ensure ai_tool has name attribute
        tool_name = self.ai_tool.name if hasattr(self.ai_tool, 'name') else "Unknown Tool"
        return f"{user_str} - {tool_name} - {self.title}"
    
    def get_messages(self) -> 'QuerySet[Message]':
        # Django automatically creates a message_set attribute for the reverse relation
        # Type ignore is needed because mypy doesn't understand Django's dynamic attributes
        return self.message_set.all().order_by('timestamp')  # type: ignore
    
    def to_json(self) -> str:
        """Convert conversation to JSON format for export"""
        data: Dict[str, Any] = {
            'id': str(self.id),
            'title': self.title,
            'ai_tool': self.ai_tool.name if hasattr(self.ai_tool, 'name') else "Unknown Tool",
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'messages': [
                {
                    'content': msg.content,
                    'is_user': msg.is_user,
                    'timestamp': msg.timestamp.isoformat()
                }
                for msg in self.get_messages()
            ]
        }
        return json.dumps(data, indent=2)


class Message(models.Model):
    """Model representing a single message in a conversation."""
    conversation: models.ForeignKey = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content: models.TextField = models.TextField()
    is_user: models.BooleanField = models.BooleanField(default=True)  # True if from user, False if from AI
    timestamp: models.DateTimeField = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        sender = "User" if self.is_user else "AI"
        return f"{sender} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class FavoritePrompt(models.Model):
    """Model for storing user's favorite prompts."""
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ai_tool: models.ForeignKey = models.ForeignKey(AITool, on_delete=models.CASCADE)
    prompt_text: models.TextField = models.TextField()
    title: models.CharField = models.CharField(max_length=255)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        username = self.user.username if hasattr(self.user, 'username') else "Unknown User"
        return f"{username} - {self.title}"


class SharedChat(models.Model):
    """Model for sharing conversations with other users or publicly."""
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation: models.ForeignKey = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    shared_by: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_chats')
    shared_with: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='received_chats'
    )
    is_public: models.BooleanField = models.BooleanField(default=False)
    access_token: models.CharField = models.CharField(max_length=64, unique=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        shared_by_name = self.shared_by.username if hasattr(self.shared_by, 'username') else "Unknown User"
        if self.is_public:
            return f"Public share by {shared_by_name}"
        elif self.shared_with:
            shared_with_name = self.shared_with.username if hasattr(self.shared_with, 'username') else "Unknown User"
            return f"Shared by {shared_by_name} with {shared_with_name}"
        else:
            return f"Private share by {shared_by_name}"


class UserFavorite(models.Model):
    """Model for storing user's favorite AI tools."""
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ai_tool: models.ForeignKey = models.ForeignKey(AITool, on_delete=models.CASCADE)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'ai_tool')
        
    def __str__(self) -> str:
        username = self.user.username if hasattr(self.user, 'username') else "Unknown User"
        tool_name = self.ai_tool.name if hasattr(self.ai_tool, 'name') else "Unknown Tool"
        return f"{username} - {tool_name}"

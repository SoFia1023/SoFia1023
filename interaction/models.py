import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
import json
from catalog.models import AITool

class Conversation(models.Model):
    """Model representing a conversation between a user and an AI tool."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='interaction_conversations'
    )
    ai_tool = models.ForeignKey(
        AITool, 
        on_delete=models.CASCADE,
        related_name='interaction_conversations'
    )
    title = models.CharField(max_length=255, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"{user_str} - {self.ai_tool.name} - {self.title}"
    
    def get_messages(self):
        return self.message_set.all().order_by('timestamp')
    
    def to_json(self):
        """Convert conversation to JSON format for export"""
        data = {
            'id': str(self.id),
            'title': self.title,
            'ai_tool': self.ai_tool.name,
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
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    is_user = models.BooleanField(default=True)  # True if from user, False if from AI
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        sender = "User" if self.is_user else "AI"
        return f"{sender} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class FavoritePrompt(models.Model):
    """Model for storing user's favorite prompts."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ai_tool = models.ForeignKey(AITool, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class SharedChat(models.Model):
    """Model for sharing conversations with other users or publicly."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_chats')
    shared_with = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='received_chats'
    )
    is_public = models.BooleanField(default=False)
    access_token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.is_public:
            return f"Public share by {self.shared_by.username}"
        elif self.shared_with:
            return f"Shared by {self.shared_by.username} with {self.shared_with.username}"
        else:
            return f"Private share by {self.shared_by.username}"


class UserFavorite(models.Model):
    """Model for storing user's favorite AI tools."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ai_tool = models.ForeignKey(AITool, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'ai_tool')
        
    def __str__(self):
        return f"{self.user.username} - {self.ai_tool.name}"

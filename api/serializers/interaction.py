"""
Serializers for the interaction app.

This module contains serializers for the interaction app models.
"""
from typing import Any, Dict, List
from rest_framework import serializers
from interaction.models import Conversation, Message, FavoritePrompt, SharedChat
from catalog.models import AITool
from django.contrib.auth import get_user_model

User = get_user_model()
from api.serializers.catalog import AIToolSerializer


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'content', 'is_from_user', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    """
    ai_tool_name = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'user', 'ai_tool', 'ai_tool_name', 'title', 
            'created_at', 'updated_at', 'message_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_ai_tool_name(self, obj: Conversation) -> str:
        """
        Get the name of the AI tool.
        
        Args:
            obj: The Conversation instance
            
        Returns:
            The name of the AI tool or 'Unknown'
        """
        return obj.ai_tool.name if obj.ai_tool else 'Unknown'
    
    def get_message_count(self, obj: Conversation) -> int:
        """
        Get the number of messages in the conversation.
        
        Args:
            obj: The Conversation instance
            
        Returns:
            The number of messages
        """
        return obj.message_set.count()


class ConversationDetailSerializer(ConversationSerializer):
    """
    Detailed serializer for the Conversation model.
    
    Includes messages and AI tool details.
    """
    messages = MessageSerializer(source='message_set', many=True, read_only=True)
    ai_tool = AIToolSerializer(read_only=True)
    
    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages']


class UserFavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for user favorites (CustomUser.favorites M2M relationship).
    """
    id = serializers.UUIDField(source='pk')
    ai_tool_name = serializers.CharField(source='name')
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model = AITool
        fields = ['id', 'user', 'ai_tool', 'ai_tool_name', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_created_at(self, obj: AITool) -> str:
        """
        Get a placeholder created_at value for compatibility.
        
        Args:
            obj: The AITool instance
            
        Returns:
            The current timestamp
        """
        from django.utils import timezone
        return timezone.now()


class FavoritePromptSerializer(serializers.ModelSerializer):
    """
    Serializer for the FavoritePrompt model.
    """
    ai_tool_names = serializers.SerializerMethodField()
    
    class Meta:
        model = FavoritePrompt
        fields = ['id', 'user', 'title', 'prompt_text', 'ai_tools', 'ai_tool_names', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_ai_tool_names(self, obj: FavoritePrompt) -> List[str]:
        """
        Get the names of the AI tools associated with this prompt.
        
        Args:
            obj: The FavoritePrompt instance
            
        Returns:
            List of AI tool names
        """
        return [tool.name for tool in obj.ai_tools.all()]


class SharedChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the SharedChat model.
    """
    conversation_title = serializers.SerializerMethodField()
    created_by_username = serializers.SerializerMethodField()
    recipient_username = serializers.SerializerMethodField()
    
    class Meta:
        model = SharedChat
        fields = [
            'id', 'conversation', 'conversation_title', 'access_token',
            'is_public', 'created_by', 'created_by_username',
            'recipient', 'recipient_username', 'created_at'
        ]
        read_only_fields = ['id', 'access_token', 'created_at']
    
    def get_conversation_title(self, obj: SharedChat) -> str:
        """
        Get the title of the conversation.
        
        Args:
            obj: The SharedChat instance
            
        Returns:
            The title of the conversation
        """
        return obj.conversation.title
    
    def get_created_by_username(self, obj: SharedChat) -> str:
        """
        Get the username of the user who created the shared chat.
        
        Args:
            obj: The SharedChat instance
            
        Returns:
            The username of the creator
        """
        return obj.created_by.username
    
    def get_recipient_username(self, obj: SharedChat) -> str:
        """
        Get the username of the recipient.
        
        Args:
            obj: The SharedChat instance
            
        Returns:
            The username of the recipient or None
        """
        return obj.recipient.username if obj.recipient else None

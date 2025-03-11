"""
Serializers for the users app.

This module contains serializers for the users app models.
"""
from typing import Any, Dict, List
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']


class UserProfileSerializer(UserSerializer):
    """
    Extended serializer for user profiles.
    
    Includes additional profile information.
    """
    favorites_count = serializers.SerializerMethodField()
    conversations_count = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['favorites_count', 'conversations_count']
    
    def get_favorites_count(self, obj: User) -> int:
        """
        Get the number of favorites for the user.
        
        Args:
            obj: The User instance
            
        Returns:
            The number of favorites
        """
        return obj.userfavorite_set.count()
    
    def get_conversations_count(self, obj: User) -> int:
        """
        Get the number of conversations for the user.
        
        Args:
            obj: The User instance
            
        Returns:
            The number of conversations
        """
        return obj.conversation_set.count()


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    
    def validate_old_password(self, value: str) -> str:
        """
        Validate that the old password is correct.
        
        Args:
            value: The old password
            
        Returns:
            The validated old password
            
        Raises:
            serializers.ValidationError: If the old password is incorrect
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value
    
    def validate_new_password(self, value: str) -> str:
        """
        Validate the new password.
        
        Args:
            value: The new password
            
        Returns:
            The validated new password
            
        Raises:
            serializers.ValidationError: If the new password is invalid
        """
        # Add additional password validation if needed
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

"""
Serializers for the catalog app.

This module contains serializers for the catalog app models.
"""
from typing import Any, Dict, List
from rest_framework import serializers
from catalog.models import AITool


class AIToolSerializer(serializers.ModelSerializer):
    """
    Serializer for the AITool model.
    """
    
    class Meta:
        model = AITool
        fields = [
            'id', 'name', 'description', 'provider', 'website', 
            'category', 'popularity', 'logo_url', 'is_free', 
            'has_api', 'pricing_model', 'pricing_url'
        ]
        read_only_fields = ['id', 'popularity']


class AIToolDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the AITool model.
    
    Includes all fields and related information.
    """
    
    class Meta:
        model = AITool
        fields = '__all__'
        read_only_fields = ['id', 'popularity']
        
    def to_representation(self, instance: AITool) -> Dict[str, Any]:
        """
        Customize the serialized representation.
        
        Args:
            instance: The AITool instance
            
        Returns:
            Dictionary with serialized data
        """
        representation = super().to_representation(instance)
        
        # Add related tools in the same category
        related_tools = AITool.objects.filter(
            category=instance.category
        ).exclude(id=instance.id)[:5]
        
        representation['related_tools'] = [
            {
                'id': str(tool.id),
                'name': tool.name,
                'description': tool.description[:100] + '...' if len(tool.description) > 100 else tool.description,
                'provider': tool.provider,
                'logo_url': tool.logo_url if tool.logo_url else '',
            }
            for tool in related_tools
        ]
        
        return representation

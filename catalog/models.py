import uuid
from django.db import models
from django.conf import settings
from typing import Any, Optional

class AITool(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    provider: models.CharField = models.CharField(max_length=255)
    endpoint: models.URLField = models.URLField()
    category: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()
    popularity: models.IntegerField = models.IntegerField()
    image: models.ImageField = models.ImageField(upload_to='ai_images/', null=True, blank=True)
    # New fields for API integration
    api_type: models.CharField = models.CharField(
        max_length=50, 
        choices=[
            ('openai', 'OpenAI API'),
            ('huggingface', 'Hugging Face API'),
            ('custom', 'Custom Integration'),
            ('none', 'No Integration')
        ],
        default='none'
    )
    api_model: models.CharField = models.CharField(max_length=100, blank=True, null=True)
    api_endpoint: models.CharField = models.CharField(max_length=255, blank=True, null=True)
    is_featured: models.BooleanField = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name

import uuid
from django.db import models
from django.conf import settings
from typing import Any, Optional

class AITool(models.Model):
    """
    Model representing an AI tool available in the catalog.
    
    This model stores information about AI tools, including their metadata,
    API integration details, and presentation information.
    
    Attributes:
        id (UUIDField): Unique identifier for the AI tool
        name (CharField): Name of the AI tool
        provider (CharField): Provider or company that created the AI tool
        endpoint (URLField): URL endpoint for accessing the AI tool
        category (CharField): Category the AI tool belongs to
        description (TextField): Detailed description of the AI tool
        popularity (IntegerField): Popularity score for ranking
        image (ImageField): Image representing the AI tool
        api_type (CharField): Type of API integration (openai, huggingface, custom, none)
        api_model (CharField): Specific model name for the API
        api_endpoint (CharField): Custom endpoint for API access
        is_featured (BooleanField): Whether this tool is featured on the homepage
    """
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
        """
        Return a string representation of the AI tool.
        
        Returns:
            str: The name of the AI tool
        """
        return self.name

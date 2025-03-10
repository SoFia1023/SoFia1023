import uuid
from django.db import models
from django.conf import settings

class AITool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    endpoint = models.URLField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    popularity = models.IntegerField()
    image = models.ImageField(upload_to='ai_images/', null=True, blank=True)
    # New fields for API integration
    api_type = models.CharField(
        max_length=50, 
        choices=[
            ('openai', 'OpenAI API'),
            ('huggingface', 'Hugging Face API'),
            ('custom', 'Custom Integration'),
            ('none', 'No Integration')
        ],
        default='none'
    )
    api_model = models.CharField(max_length=100, blank=True, null=True)
    api_endpoint = models.CharField(max_length=255, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class UserFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ai_tool = models.ForeignKey(AITool, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'ai_tool')
        
    def __str__(self):
        return f"{self.user.username} - {self.ai_tool.name}"

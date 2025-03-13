import uuid
from django.db import models
from django.conf import settings
from typing import Any, Optional
from django.db.models import Avg

class AITool(models.Model):
    """
    Model representing an AI tool available in the catalog.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    endpoint = models.URLField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='ai_images/', null=True, blank=True)
    popularity = models.FloatField(default=0)

    def update_popularity(self):
        """Actualiza la popularidad basada en el promedio de calificaciones"""
        avg = self.ratings.aggregate(Avg('stars'))['stars__avg']
        self.popularity = avg if avg else 0
        self.save()
    
    
    # API integration fields
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
    

    def get_average_rating(self):
        """Calcula el promedio de calificación en estrellas."""
        avg_rating = self.ratings.aggregate(Avg('stars'))['stars__avg']
        return round(avg_rating, 2) if avg_rating else "There are no ratings yet."
    

# Make a rating with stars and reviews.  
class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.CustomUser',  # Usar referencia por string
        on_delete=models.CASCADE,
        related_name='ai_ratings'
    )
    ai_tool = models.ForeignKey(AITool, on_delete=models.CASCADE, related_name="ratings")
    stars = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ai_tool')  # Prevents a user from rating the same AI twice

    def __str__(self):
        return f"{self.user.first_name} ({self.user.id}) - {self.ai_tool.name} - {self.stars}⭐"

from django.contrib.auth.models import AbstractUser
from django.db import models
from typing import List

class CustomUser(AbstractUser):
    email: models.EmailField = models.EmailField(unique=True, help_text="User email")
    first_name: models.CharField = models.CharField(max_length=255, help_text="User first name")  

    favorites: models.ManyToManyField = models.ManyToManyField(
        'catalog.AITool',  
        related_name='favorited_by',
        blank=True,  # Allows the field to be empty
        help_text="User's favorite AI tools"
    )

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username', 'first_name']  

    def __str__(self) -> str:
        return self.email

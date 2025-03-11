"""
Core models module.

This module contains base model classes that can be inherited by models in other apps.
"""
from typing import Any, Optional, Type, TypeVar, cast
import uuid
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """
    An abstract base model that provides self-updating created and modified fields.
    
    Attributes:
        created_at: The datetime when the object was created
        updated_at: The datetime when the object was last updated
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    
    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    An abstract base model that uses UUID as primary key.
    
    Attributes:
        id: UUID primary key field
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True


class SluggedModel(models.Model):
    """
    An abstract base model that automatically generates a slug field.
    
    Attributes:
        slug: A slug field generated from the slugify_field_name
    """
    slug = models.SlugField(max_length=255, unique=True)
    slugify_field_name = 'name'  # Field to base the slug on, override in subclasses
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Override the save method to automatically generate a slug if not provided.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
    
    def _generate_unique_slug(self) -> str:
        """
        Generate a unique slug based on the slugify_field_name.
        
        Returns:
            A unique slug string
        """
        slugify_field_value = getattr(self, self.slugify_field_name)
        slug = slugify(slugify_field_value)
        unique_slug = slug
        
        # Check if the slug already exists and make it unique if needed
        ModelClass = self.__class__
        extension = 1
        
        while ModelClass.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{extension}"
            extension += 1
            
        return unique_slug
    
    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """
    An abstract base model for content that can be published or unpublished.
    
    Attributes:
        is_published: Whether the content is published
        published_at: When the content was published
    """
    is_published = models.BooleanField(default=False, verbose_name="Published")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Published at")
    
    def publish(self) -> None:
        """
        Publish the content by setting is_published to True and published_at to now.
        """
        self.is_published = True
        self.published_at = timezone.now()
        self.save(update_fields=['is_published', 'published_at'])
    
    def unpublish(self) -> None:
        """
        Unpublish the content by setting is_published to False.
        """
        self.is_published = False
        self.save(update_fields=['is_published'])
    
    class Meta:
        abstract = True

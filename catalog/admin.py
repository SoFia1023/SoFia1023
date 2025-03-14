from django.contrib import admin
from .models import AITool, Rating
from inspireIA.admin import admin_site
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpRequest
from django.core.management import call_command
from typing import List, Dict, Any, Optional, Union, Tuple, Set, Callable, Type, cast
from django.db.models.query import QuerySet



class AIToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'category', 'popularity', 'api_type', 'is_featured', 'view_favorites_count', 'image_preview')
    list_filter = ('category', 'api_type', 'is_featured', 'provider')
    search_fields = ('name', 'provider', 'description', 'category')
    list_editable = ('is_featured',)
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'provider', 'category', 'description', 'popularity', 'image', 'endpoint')
        }),
        ('API Integration', {
            'fields': ('api_type', 'api_model', 'api_endpoint', 'is_featured'),
            'classes': ('collapse',),
            'description': 'Configure external API integrations for this AI tool'
        }),
    )
    readonly_fields = ('id',)
    
    actions = [
        'feature_tools', 
        'unfeature_tools', 
        'increase_popularity', 
        'reset_popularity',
        'duplicate_tools',
        'refresh_logos'
    ]

    
    def get_queryset(self, request: HttpRequest) -> QuerySet[AITool]:
        """Optimize query by annotating with favorites count"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('favorited_by')
    
    def view_favorites_count(self, obj: AITool) -> str:
        """Display the number of users who have favorited this tool"""
        count = obj.favorited_by.count()
        url = reverse('admin:users_customuser_changelist') + f'?favorites__id__exact={obj.id}'
        return format_html('<a href="{}">{} users</a>', url, count)
    view_favorites_count.short_description = 'Favorited by'
    
    def image_preview(self, obj: AITool) -> str:
        """Display a thumbnail of the AI tool image"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: contain; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        # If no image, display a placeholder with the first letter of the tool name
        return format_html(
            '<div style="width:50px; height:50px; border-radius:8px; background:linear-gradient(135deg, #5f4b8b, #9168c0); color:white; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:20px;">{}</div>',
            obj.name[0].upper()
        )
    image_preview.short_description = 'Logo'
    
    def feature_tools(self, request, queryset):
        """Mark selected tools as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request, 
            f"{updated} AI {'tool was' if updated == 1 else 'tools were'} marked as featured and will appear prominently in the catalog.", 
            messages.SUCCESS
        )
    feature_tools.short_description = "✨ Feature selected AI tools"
    
    def unfeature_tools(self, request, queryset):
        """Unmark selected tools as featured"""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request, 
            f"{updated} AI {'tool was' if updated == 1 else 'tools were'} unmarked as featured and will no longer appear in featured sections.", 
            messages.SUCCESS
        )
    unfeature_tools.short_description = "⬇️ Unfeature selected AI tools"
    
    def increase_popularity(self, request, queryset):
        """Increase popularity of selected tools by 10"""
        for tool in queryset:
            tool.popularity += 10
            tool.save()
        self.message_user(
            request, 
            f"Increased popularity for {queryset.count()} AI {'tool' if queryset.count() == 1 else 'tools'} by 10 points.", 
            messages.SUCCESS
        )
    increase_popularity.short_description = "📈 Increase popularity by 10"
    
    def reset_popularity(self, request, queryset):
        """Reset popularity of selected tools to 0"""
        updated = queryset.update(popularity=0)
        self.message_user(
            request, 
            f"Reset popularity for {updated} AI {'tool' if updated == 1 else 'tools'} to 0.", 
            messages.SUCCESS
        )
    reset_popularity.short_description = "🔄 Reset popularity to 0"
    
    def duplicate_tools(self, request, queryset):
        """Duplicate selected AI tools"""
        count = 0
        for tool in queryset:
            # Create a copy of the tool
            tool_copy = AITool.objects.create(
                name=f"Copy of {tool.name}",
                provider=tool.provider,
                endpoint=tool.endpoint,
                category=tool.category,
                description=tool.description,
                popularity=0,  # Start with 0 popularity
                api_type=tool.api_type,
                api_model=tool.api_model,
                api_endpoint=tool.api_endpoint,
                is_featured=False  # New copies are not featured by default
            )
            
            # If there's an image, we need to handle it separately
            if tool.image:
                # This will create a copy of the image file
                tool_copy.image = tool.image
                tool_copy.save()
                
            count += 1
            
        self.message_user(
            request, 
            f"Successfully duplicated {count} AI {'tool' if count == 1 else 'tools'}. The new copies have 0 popularity and are not featured.", 
            messages.SUCCESS
        )
    duplicate_tools.short_description = "🔄 Duplicate selected AI tools"
    
    def refresh_logos(self, request, queryset):
        """Refresh logos for selected AI tools using high-quality sources"""
        try:
            # Note which tools were selected
            selected_names = list(queryset.values_list('name', flat=True))
            
            # We'll use our management command to refresh logos
            call_command('fetch_ai_tool_logos', force=True)
            
            # Report success
            self.message_user(
                request,
                f"Successfully refreshed logos for {len(selected_names)} AI tools: {', '.join(selected_names)}.",
                messages.SUCCESS
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error refreshing logos: {str(e)}",
                messages.ERROR
            )
    refresh_logos.short_description = "🖼️ Refresh logos for selected tools"


class RatingAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('get_user_info', 'get_tool_info', 'stars', 'comment', 'created_at')
    
    # Filtering and search
    list_filter = ('stars', 'created_at')
    search_fields = ('user__email', 'ai_tool__name', 'comment')
    
    # Read-only fields
    readonly_fields = ('id', 'created_at')
    
    # Field organization
    fieldsets = (
        ('Rating Information', {
            'fields': ('user', 'ai_tool', 'stars')
        }),
        ('Review', {
            'fields': ('comment',),
            'description': 'Optional text review'
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        })
    )

    def get_user_info(self, obj):
        """Display user ID and email"""
        return f"{obj.user.email} (ID: {obj.user.id})"
    get_user_info.short_description = 'User'

    def get_tool_info(self, obj):
        """Display tool name and ID"""
        return f"{obj.ai_tool.name} (ID: {obj.ai_tool.id})"
    get_tool_info.short_description = 'AI Tool'

    
# Register models with our custom admin site
admin_site.register(AITool, AIToolAdmin)

# Also register with the default admin site for backward compatibility
admin.site.register(AITool, AIToolAdmin)
admin.site.register(Rating, RatingAdmin)


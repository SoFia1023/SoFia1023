from django.contrib import admin
from .models import Conversation, Message, FavoritePrompt, SharedChat, UserFavorite
from inspireIA.admin import admin_site
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
import json
import csv
from django.http import HttpResponse
import datetime

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('timestamp',)
    fields = ('is_user', 'content_preview', 'timestamp')
    
    def content_preview(self, obj):
        """Display a preview of the message content"""
        if len(obj.content) > 100:
            return obj.content[:100] + '...'
        return obj.content
    content_preview.short_description = 'Content'
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'ai_tool', 'message_count', 'created_at', 'updated_at')
    list_filter = ('ai_tool', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username', 'user__email', 'ai_tool__name')
    readonly_fields = ('created_at', 'updated_at', 'id')
    date_hierarchy = 'created_at'
    inlines = [MessageInline]
    raw_id_fields = ('user', 'ai_tool')
    
    actions = [
        'export_conversations_json', 
        'export_conversations_csv',
        'mark_as_important',
        'archive_conversations'
    ]
    
    def get_queryset(self, request):
        """Optimize query by prefetching related objects"""
        return super().get_queryset(request).select_related('user', 'ai_tool').prefetch_related('message_set')
    
    def message_count(self, obj):
        """Display the number of messages in this conversation"""
        count = obj.message_set.count()
        return count
    message_count.short_description = 'Messages'
    
    def export_conversations_json(self, request, queryset):
        """Export selected conversations to JSON"""
        from django.http import HttpResponse
        
        conversations = []
        for conversation in queryset:
            conversations.append({
                'id': str(conversation.id),
                'title': conversation.title,
                'user': conversation.user.username if conversation.user else 'Anonymous',
                'ai_tool': conversation.ai_tool.name,
                'created_at': conversation.created_at.isoformat(),
                'updated_at': conversation.updated_at.isoformat(),
                'messages': [
                    {
                        'content': msg.content,
                        'is_user': msg.is_user,
                        'timestamp': msg.timestamp.isoformat()
                    }
                    for msg in conversation.message_set.all().order_by('timestamp')
                ]
            })
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        response = HttpResponse(json.dumps(conversations, indent=2), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="conversations_{timestamp}.json"'
        
        self.message_user(
            request, 
            f"Exported {len(conversations)} {'conversation' if len(conversations) == 1 else 'conversations'} to JSON.", 
            messages.SUCCESS
        )
        return response
    export_conversations_json.short_description = "📤 Export to JSON"
    
    def export_conversations_csv(self, request, queryset):
        """Export selected conversations to CSV"""
        response = HttpResponse(content_type='text/csv')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="conversations_{timestamp}.csv"'
        
        writer = csv.writer(response)
        # Write header
        writer.writerow(['Conversation ID', 'Title', 'User', 'AI Tool', 'Created At', 'Message Type', 'Message Content', 'Message Timestamp'])
        
        # Write data
        for conversation in queryset:
            user_name = conversation.user.username if conversation.user else 'Anonymous'
            
            for message in conversation.message_set.all().order_by('timestamp'):
                writer.writerow([
                    str(conversation.id),
                    conversation.title,
                    user_name,
                    conversation.ai_tool.name,
                    conversation.created_at.isoformat(),
                    'User' if message.is_user else 'AI',
                    message.content,
                    message.timestamp.isoformat()
                ])
        
        self.message_user(
            request, 
            f"Exported {queryset.count()} {'conversation' if queryset.count() == 1 else 'conversations'} to CSV.", 
            messages.SUCCESS
        )
        return response
    export_conversations_csv.short_description = "📄 Export to CSV"
    
    def mark_as_important(self, request, queryset):
        """Mark selected conversations as important by adding '[IMPORTANT]' to the title"""
        count = 0
        for conversation in queryset:
            if not conversation.title.startswith('[IMPORTANT]'):
                conversation.title = f'[IMPORTANT] {conversation.title}'
                conversation.save()
                count += 1
        
        self.message_user(
            request, 
            f"Marked {count} {'conversation' if count == 1 else 'conversations'} as important.", 
            messages.SUCCESS
        )
    mark_as_important.short_description = "⭐ Mark as important"
    
    def archive_conversations(self, request, queryset):
        """Archive selected conversations by adding '[ARCHIVED]' to the title"""
        count = 0
        for conversation in queryset:
            if not conversation.title.startswith('[ARCHIVED]'):
                conversation.title = f'[ARCHIVED] {conversation.title}'
                conversation.save()
                count += 1
        
        self.message_user(
            request, 
            f"Archived {count} {'conversation' if count == 1 else 'conversations'}.", 
            messages.SUCCESS
        )
    archive_conversations.short_description = "📦 Archive conversations"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation_link', 'is_user', 'content_preview', 'timestamp')
    list_filter = ('is_user', 'timestamp', 'conversation__ai_tool')
    search_fields = ('content', 'conversation__title', 'conversation__user__username')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    raw_id_fields = ('conversation',)
    
    def get_queryset(self, request):
        """Optimize query by prefetching related objects"""
        return super().get_queryset(request).select_related('conversation', 'conversation__user', 'conversation__ai_tool')
    
    def content_preview(self, obj):
        """Display a preview of the message content"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def conversation_link(self, obj):
        """Display a link to the conversation"""
        url = reverse('admin:interaction_conversation_change', args=[obj.conversation.id])
        return format_html('<a href="{}">{}</a>', url, obj.conversation.title)
    conversation_link.short_description = 'Conversation'
    conversation_link.admin_order_field = 'conversation__title'

@admin.register(FavoritePrompt)
class FavoritePromptAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'ai_tool', 'prompt_preview', 'created_at')
    list_filter = ('ai_tool', 'created_at')
    search_fields = ('title', 'prompt_text', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'id')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'ai_tool')
    
    def get_queryset(self, request):
        """Optimize query by prefetching related objects"""
        return super().get_queryset(request).select_related('user', 'ai_tool')
    
    def prompt_preview(self, obj):
        """Display a preview of the prompt text"""
        return obj.prompt_text[:50] + '...' if len(obj.prompt_text) > 50 else obj.prompt_text
    prompt_preview.short_description = 'Prompt Preview'

@admin.register(SharedChat)
class SharedChatAdmin(admin.ModelAdmin):
    list_display = ('conversation_link', 'shared_by', 'shared_with', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('conversation__title', 'shared_by__username', 'shared_with__username')
    readonly_fields = ('created_at', 'access_token', 'id')
    date_hierarchy = 'created_at'
    raw_id_fields = ('conversation', 'shared_by', 'shared_with')
    
    def get_queryset(self, request):
        """Optimize query by prefetching related objects"""
        return super().get_queryset(request).select_related('conversation', 'shared_by', 'shared_with')
    
    def conversation_link(self, obj):
        """Display a link to the conversation"""
        url = reverse('admin:interaction_conversation_change', args=[obj.conversation.id])
        return format_html('<a href="{}">{}</a>', url, obj.conversation.title)
    conversation_link.short_description = 'Conversation'
    conversation_link.admin_order_field = 'conversation__title'

@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'ai_tool', 'created_at')
    list_filter = ('created_at', 'ai_tool__category')
    search_fields = ('user__username', 'user__email', 'ai_tool__name')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'ai_tool')
    
    def get_queryset(self, request):
        """Optimize query by prefetching related objects"""
        return super().get_queryset(request).select_related('user', 'ai_tool')

# Register with our custom admin site
admin_site.register(Conversation, ConversationAdmin)
admin_site.register(Message, MessageAdmin)
admin_site.register(FavoritePrompt, FavoritePromptAdmin)
admin_site.register(SharedChat, SharedChatAdmin)
admin_site.register(UserFavorite, UserFavoriteAdmin)

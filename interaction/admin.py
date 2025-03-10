from django.contrib import admin
from .models import Conversation, Message, FavoritePrompt, SharedChat

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('timestamp',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'ai_tool', 'created_at', 'updated_at')
    list_filter = ('ai_tool', 'created_at')
    search_fields = ('title', 'user__username', 'ai_tool__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'is_user', 'content_preview', 'timestamp')
    list_filter = ('is_user', 'timestamp', 'conversation__ai_tool')
    search_fields = ('content', 'conversation__title')
    readonly_fields = ('timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(FavoritePrompt)
class FavoritePromptAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'ai_tool', 'created_at')
    list_filter = ('ai_tool', 'created_at')
    search_fields = ('title', 'prompt_text', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(SharedChat)
class SharedChatAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'shared_by', 'shared_with', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('conversation__title', 'shared_by__username', 'shared_with__username')
    readonly_fields = ('created_at', 'access_token')

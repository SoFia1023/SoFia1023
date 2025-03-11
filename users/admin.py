from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.models import Group, Permission
from inspireIA.admin import admin_site
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
import csv
import datetime
from typing import List, Dict, Any, Optional, Union, Tuple, Set, Callable, Type, cast
from django.db.models.query import QuerySet

# Register your models here.
#admin.site.register(CustomUser)  #



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'is_staff', 'get_groups', 'favorite_count', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name')
    filter_horizontal = ('groups', 'user_permissions', 'favorites')
    date_hierarchy = 'date_joined'
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('AI Preferences', {'fields': ('favorites',)}),
    )
    
    actions = [
        'activate_users', 
        'deactivate_users', 
        'add_to_regular_users', 
        'add_to_content_managers',
        'add_to_administrators',
        'remove_from_all_groups',
        'export_users_csv',
        'grant_staff_status',
        'revoke_staff_status'
    ]
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[CustomUser]:
        """Optimize query by prefetching related objects"""
        return super().get_queryset(request).prefetch_related('groups', 'favorites')
    
    def get_groups(self, obj: CustomUser) -> str:
        """Return a comma-separated list of the user's groups."""
        groups = [group.name for group in obj.groups.all()]
        if not groups:
            return "No groups"
        return ", ".join(groups)
    get_groups.short_description = 'Groups'
    
    def favorite_count(self, obj):
        """Display the number of AI tools favorited by this user"""
        count = obj.favorites.count()
        if count > 0:
            url = reverse('admin:catalog_aitool_changelist')
            return format_html('<a href="{}">{} tools</a>', url, count)
        return "0 tools"
    favorite_count.short_description = 'Favorites'
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request, 
            f"{updated} {'user was' if updated == 1 else 'users were'} activated successfully.", 
            messages.SUCCESS
        )
    activate_users.short_description = "✅ Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request, 
            f"{updated} {'user was' if updated == 1 else 'users were'} deactivated successfully.", 
            messages.SUCCESS
        )
    deactivate_users.short_description = "❌ Deactivate selected users"
    
    def add_to_regular_users(self, request, queryset):
        """Add selected users to the Regular Users group"""
        try:
            regular_users_group = Group.objects.get(name='Regular Users')
            count = 0
            for user in queryset:
                if regular_users_group not in user.groups.all():
                    user.groups.add(regular_users_group)
                    count += 1
            self.message_user(
                request, 
                f"{count} {'user was' if count == 1 else 'users were'} added to Regular Users group.", 
                messages.SUCCESS
            )
        except Group.DoesNotExist:
            self.message_user(request, "Regular Users group does not exist.", messages.ERROR)
    add_to_regular_users.short_description = "👤 Add to Regular Users group"
    
    def add_to_content_managers(self, request, queryset):
        """Add selected users to the Content Managers group"""
        try:
            content_managers_group = Group.objects.get(name='Content Managers')
            count = 0
            for user in queryset:
                if content_managers_group not in user.groups.all():
                    if not user.is_staff:
                        user.is_staff = True
                        user.save()
                    user.groups.add(content_managers_group)
                    count += 1
            self.message_user(
                request, 
                f"{count} {'user was' if count == 1 else 'users were'} added to Content Managers group and granted staff status.", 
                messages.SUCCESS
            )
        except Group.DoesNotExist:
            self.message_user(request, "Content Managers group does not exist.", messages.ERROR)
    add_to_content_managers.short_description = "📊 Add to Content Managers group"
    
    def add_to_administrators(self, request, queryset):
        """Add selected users to the Administrators group"""
        try:
            admin_group = Group.objects.get(name='Administrators')
            count = 0
            for user in queryset:
                if admin_group not in user.groups.all():
                    if not user.is_staff:
                        user.is_staff = True
                    if not user.is_superuser:
                        user.is_superuser = True
                    user.save()
                    user.groups.add(admin_group)
                    count += 1
            self.message_user(
                request, 
                f"{count} {'user was' if count == 1 else 'users were'} added to Administrators group and granted staff and superuser status.", 
                messages.SUCCESS
            )
        except Group.DoesNotExist:
            self.message_user(request, "Administrators group does not exist.", messages.ERROR)
    add_to_administrators.short_description = "🔑 Add to Administrators group"
    
    def remove_from_all_groups(self, request, queryset):
        """Remove selected users from all groups"""
        count = 0
        for user in queryset:
            if user.groups.exists():
                user.groups.clear()
                count += 1
        self.message_user(
            request, 
            f"{count} {'user was' if count == 1 else 'users were'} removed from all groups.", 
            messages.SUCCESS
        )
    remove_from_all_groups.short_description = "🗑️ Remove from all groups"
    
    def export_users_csv(self, request, queryset):
        """Export selected users to CSV"""
        response = HttpResponse(content_type='text/csv')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="users_{timestamp}.csv"'
        
        writer = csv.writer(response)
        # Write header
        writer.writerow(['Username', 'Email', 'First Name', 'Is Staff', 'Is Superuser', 'Is Active', 'Groups', 'Date Joined', 'Last Login'])
        
        # Write data
        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                'Yes' if user.is_staff else 'No',
                'Yes' if user.is_superuser else 'No',
                'Yes' if user.is_active else 'No',
                ', '.join([group.name for group in user.groups.all()]),
                user.date_joined.isoformat() if user.date_joined else '',
                user.last_login.isoformat() if user.last_login else ''
            ])
        
        self.message_user(
            request, 
            f"Exported {queryset.count()} {'user' if queryset.count() == 1 else 'users'} to CSV.", 
            messages.SUCCESS
        )
        return response
    export_users_csv.short_description = "📄 Export users to CSV"
    
    def grant_staff_status(self, request, queryset):
        """Grant staff status to selected users"""
        count = 0
        for user in queryset:
            if not user.is_staff:
                user.is_staff = True
                user.save()
                count += 1
        self.message_user(
            request, 
            f"Granted staff status to {count} {'user' if count == 1 else 'users'}.", 
            messages.SUCCESS
        )
    grant_staff_status.short_description = "👔 Grant staff status"
    
    def revoke_staff_status(self, request, queryset):
        """Revoke staff status from selected users"""
        count = 0
        for user in queryset:
            if user.is_staff and not user.is_superuser:  # Don't revoke from superusers
                user.is_staff = False
                user.save()
                count += 1
        self.message_user(
            request, 
            f"Revoked staff status from {count} {'user' if count == 1 else 'users'}. Superusers were not affected.", 
            messages.SUCCESS
        )
    revoke_staff_status.short_description = "👕 Revoke staff status"

# Customize the Group admin
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_count', 'get_permission_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    actions = ['export_group_permissions', 'copy_permissions_to_selected']
    
    def get_queryset(self, request):
        """Optimize query by prefetching related objects"""
        return super().get_queryset(request).prefetch_related('user_set', 'permissions')
    
    def get_user_count(self, obj):
        """Return the number of users in this group."""
        count = obj.user_set.count()
        if count > 0:
            url = reverse('admin:users_customuser_changelist') + f'?groups__id__exact={obj.id}'
            return format_html('<a href="{}">{} users</a>', url, count)
        return "0 users"
    get_user_count.short_description = 'Users'
    
    def get_permission_count(self, obj):
        """Return the number of permissions in this group."""
        count = obj.permissions.count()
        return f"{count} permissions"
    get_permission_count.short_description = 'Permissions'
    
    def export_group_permissions(self, request, queryset):
        """Export permissions for selected groups to CSV"""
        response = HttpResponse(content_type='text/csv')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="group_permissions_{timestamp}.csv"'
        
        writer = csv.writer(response)
        # Write header
        writer.writerow(['Group', 'Permission', 'Content Type'])
        
        # Write data
        for group in queryset:
            for permission in group.permissions.all().select_related('content_type'):
                writer.writerow([
                    group.name,
                    permission.name,
                    permission.content_type.app_label + '.' + permission.content_type.model
                ])
        
        self.message_user(
            request, 
            f"Exported permissions for {queryset.count()} {'group' if queryset.count() == 1 else 'groups'} to CSV.", 
            messages.SUCCESS
        )
        return response
    export_group_permissions.short_description = "📄 Export permissions to CSV"
    
    def copy_permissions_to_selected(self, request, queryset):
        """Copy permissions from the first selected group to all other selected groups"""
        if queryset.count() < 2:
            self.message_user(request, "You must select at least two groups to copy permissions.", messages.ERROR)
            return
        
        source_group = queryset.first()
        target_groups = queryset.exclude(id=source_group.id)
        
        permissions = source_group.permissions.all()
        
        for group in target_groups:
            group.permissions.set(permissions)
        
        self.message_user(
            request, 
            f"Copied {permissions.count()} permissions from '{source_group.name}' to {target_groups.count()} other {'group' if target_groups.count() == 1 else 'groups'}.", 
            messages.SUCCESS
        )
    copy_permissions_to_selected.short_description = "📋 Copy permissions to selected groups"

# Register with our custom admin site
admin_site.register(CustomUser, CustomUserAdmin)
admin_site.register(Group, GroupAdmin)

# Also register with the default admin site for backward compatibility
admin.site.register(CustomUser, CustomUserAdmin)

# Unregister the default Group admin and register our custom one
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

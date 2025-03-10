from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.db.models import Count, Sum, F, Q, Avg, Case, When, IntegerField
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncMonth

class InspireIAAdminSite(AdminSite):
    # Change the admin site title, header, and index title
    site_title = _('InspireIA Admin')
    site_header = _('InspireIA Administration')
    index_title = _('Platform Management')
    
    def index(self, request, extra_context=None):
        """
        Override the index view to include dashboard statistics.
        """
        # Get statistics for the dashboard
        stats = self.get_dashboard_stats()
        
        # Combine with any extra context
        context = {
            **stats,
            **(extra_context or {}),
        }
        
        return super().index(request, extra_context=context)
    
    def get_dashboard_stats(self):
        """
        Get statistics for the dashboard.
        """
        from django.contrib.auth import get_user_model
        from catalog.models import AITool
        from interaction.models import Conversation, Message, UserFavorite, SharedChat, FavoritePrompt
        
        User = get_user_model()
        
        # Basic counts
        user_count = User.objects.count()
        ai_tool_count = AITool.objects.count()
        conversation_count = Conversation.objects.count()
        message_count = Message.objects.count()
        
        # Get date for "last 7 days" calculations
        last_week = timezone.now() - timedelta(days=7)
        last_month = timezone.now() - timedelta(days=30)
        
        # Active users (users with conversations in the last 7 days)
        active_users = User.objects.filter(
            interaction_conversations__created_at__gte=last_week
        ).distinct().count()
        
        # New users in the last 7 days
        new_users = User.objects.filter(
            date_joined__gte=last_week
        ).count()
        
        # New conversations in the last 7 days
        new_conversations = Conversation.objects.filter(
            created_at__gte=last_week
        ).count()
        
        # Popular AI tools (based on popularity field)
        popular_ai_tools = list(AITool.objects.order_by('-popularity')[:5].values('name', 'popularity'))
        
        # Most used AI tools (based on conversations)
        most_used_tools = list(AITool.objects.annotate(
            usage_count=Count('interaction_conversations')
        ).order_by('-usage_count')[:5].values('name', 'usage_count'))
        
        # Most favorited AI tools
        most_favorited = list(AITool.objects.annotate(
            favorite_count=Count('favorited_by')
        ).order_by('-favorite_count')[:5].values('name', 'favorite_count'))
        
        # Category distribution
        category_distribution = list(AITool.objects.values('category').annotate(
            count=Count('id')
        ).order_by('-count'))
        
        # API type distribution
        api_type_distribution = list(AITool.objects.values('api_type').annotate(
            count=Count('id')
        ).order_by('-count'))
        
        # NEW STATISTICS
        
        # Average messages per conversation
        avg_messages_per_conversation = Message.objects.count() / max(Conversation.objects.count(), 1)
        
        # Most active users (based on number of conversations)
        most_active_users = list(User.objects.annotate(
            conversation_count=Count('interaction_conversations')
        ).order_by('-conversation_count')[:5].values('username', 'conversation_count'))
        
        # User growth over time (monthly registrations)
        user_growth = list(User.objects.annotate(
            month=TruncMonth('date_joined')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('-month')[:6])
        
        # Reverse the order to show oldest to newest
        user_growth.reverse()
        
        # Format the month names
        for entry in user_growth:
            entry['month_name'] = entry['month'].strftime('%b %Y')
        
        # AI tool usage trends (last 30 days vs previous 30 days)
        current_period_usage = Conversation.objects.filter(
            created_at__gte=last_month
        ).count()
        
        previous_period = timezone.now() - timedelta(days=60)
        previous_period_usage = Conversation.objects.filter(
            created_at__gte=previous_period,
            created_at__lt=last_month
        ).count()
        
        usage_trend_percentage = 0
        if previous_period_usage > 0:
            usage_trend_percentage = ((current_period_usage - previous_period_usage) / previous_period_usage) * 100
        
        # Shared conversations statistics
        total_shared = SharedChat.objects.count()
        public_shares = SharedChat.objects.filter(is_public=True).count()
        private_shares = total_shared - public_shares
        
        # Favorite prompts statistics
        favorite_prompts_count = FavoritePrompt.objects.count()
        prompts_per_tool = list(FavoritePrompt.objects.values('ai_tool__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5])
        
        # Featured AI tools
        featured_tools = list(AITool.objects.filter(
            is_featured=True
        ).values('name', 'category')[:5])
        
        # User engagement metrics
        user_engagement = {
            'total_conversations': conversation_count,
            'avg_messages_per_conversation': round(avg_messages_per_conversation, 2),
            'total_messages': message_count,
            'conversations_last_7_days': new_conversations,
            'messages_last_7_days': Message.objects.filter(timestamp__gte=last_week).count(),
        }
        
        return {
            'user_count': user_count,
            'ai_tool_count': ai_tool_count,
            'conversation_count': conversation_count,
            'message_count': message_count,
            'active_users': active_users,
            'new_users': new_users,
            'new_conversations': new_conversations,
            'popular_ai_tools': popular_ai_tools,
            'most_used_tools': most_used_tools,
            'most_favorited': most_favorited,
            'category_distribution': category_distribution,
            'api_type_distribution': api_type_distribution,
            # New statistics
            'avg_messages_per_conversation': round(avg_messages_per_conversation, 2),
            'most_active_users': most_active_users,
            'user_growth': user_growth,
            'usage_trend_percentage': round(usage_trend_percentage, 2),
            'total_shared': total_shared,
            'public_shares': public_shares,
            'private_shares': private_shares,
            'favorite_prompts_count': favorite_prompts_count,
            'prompts_per_tool': prompts_per_tool,
            'featured_tools': featured_tools,
            'user_engagement': user_engagement,
        }
    
    # Group models by app
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        
        # Sort the apps alphabetically
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        # Sort the models alphabetically within each app
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
            
        # Define app groups and their order
        app_groups = {
            'Authentication and Authorization': ['auth'],
            'Catalog': ['catalog'],
            'User Interactions': ['interaction'],
            'Users': ['users'],
        }
        
        # Organize apps into groups
        grouped_app_list = []
        for group_name, app_names in app_groups.items():
            group = {
                'name': group_name,
                'app_label': group_name.lower().replace(' ', '_'),
                'app_url': '#',
                'has_module_perms': True,
                'models': [],
            }
            
            for app in app_list:
                if app['app_label'] in app_names:
                    group['models'].extend(app['models'])
            
            if group['models']:
                grouped_app_list.append(group)
        
        # Add any remaining apps to an "Other" group
        remaining_apps = [
            app for app in app_list 
            if not any(app['app_label'] in app_names for app_names in app_groups.values())
        ]
        
        if remaining_apps:
            other_group = {
                'name': 'Other',
                'app_label': 'other',
                'app_url': '#',
                'has_module_perms': True,
                'models': [],
            }
            
            for app in remaining_apps:
                other_group['models'].extend(app['models'])
            
            grouped_app_list.append(other_group)
        
        return grouped_app_list

# Create an instance of the custom admin site
admin_site = InspireIAAdminSite(name='inspire_admin') 
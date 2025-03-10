from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.db.models import Count

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
        from interaction.models import Conversation, Message
        
        User = get_user_model()
        
        return {
            'user_count': User.objects.count(),
            'ai_tool_count': AITool.objects.count(),
            'conversation_count': Conversation.objects.count(),
            'message_count': Message.objects.count(),
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
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import AITool
from interaction.models import UserFavorite
from interaction.models import Conversation, Message, FavoritePrompt, SharedChat
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Create user groups with appropriate permissions'

    def handle(self, *args, **options):
        # Clear existing groups to avoid duplicates
        Group.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted existing groups'))

        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Administrators')
        content_manager_group, created = Group.objects.get_or_create(name='Content Managers')
        regular_user_group, created = Group.objects.get_or_create(name='Regular Users')

        # Get content types for our models
        aitool_ct = ContentType.objects.get_for_model(AITool)
        userfavorite_ct = ContentType.objects.get_for_model(UserFavorite)
        conversation_ct = ContentType.objects.get_for_model(Conversation)
        message_ct = ContentType.objects.get_for_model(Message)
        favoriteprompt_ct = ContentType.objects.get_for_model(FavoritePrompt)
        sharedchat_ct = ContentType.objects.get_for_model(SharedChat)
        user_ct = ContentType.objects.get_for_model(CustomUser)

        # Get all permissions
        all_permissions = Permission.objects.all()
        
        # Assign permissions to Administrators (all permissions)
        admin_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS(f'Added all permissions to Administrators group'))

        # Assign permissions to Content Managers
        # They can manage AI tools and view user interactions, but not manage users
        content_manager_permissions = []
        
        # AI Tool permissions (full access)
        content_manager_permissions.extend(
            Permission.objects.filter(content_type=aitool_ct)
        )
        
        # User Favorite permissions (view only)
        content_manager_permissions.extend(
            Permission.objects.filter(
                content_type=userfavorite_ct, 
                codename__in=['view_userfavorite']
            )
        )
        
        # Conversation permissions (view only)
        content_manager_permissions.extend(
            Permission.objects.filter(
                content_type=conversation_ct,
                codename__in=['view_conversation']
            )
        )
        
        # Message permissions (view only)
        content_manager_permissions.extend(
            Permission.objects.filter(
                content_type=message_ct,
                codename__in=['view_message']
            )
        )
        
        # Favorite Prompt permissions (view only)
        content_manager_permissions.extend(
            Permission.objects.filter(
                content_type=favoriteprompt_ct,
                codename__in=['view_favoriteprompt']
            )
        )
        
        # Shared Chat permissions (view only)
        content_manager_permissions.extend(
            Permission.objects.filter(
                content_type=sharedchat_ct,
                codename__in=['view_sharedchat']
            )
        )
        
        # User permissions (view only)
        content_manager_permissions.extend(
            Permission.objects.filter(
                content_type=user_ct,
                codename__in=['view_customuser']
            )
        )
        
        content_manager_group.permissions.set(content_manager_permissions)
        self.stdout.write(self.style.SUCCESS(
            f'Added {len(content_manager_permissions)} permissions to Content Managers group'
        ))

        # Assign permissions to Regular Users
        # They can only manage their own data
        regular_user_permissions = []
        
        # AI Tool permissions (view only)
        regular_user_permissions.extend(
            Permission.objects.filter(
                content_type=aitool_ct,
                codename__in=['view_aitool']
            )
        )
        
        # User Favorite permissions (add, change, delete, view)
        regular_user_permissions.extend(
            Permission.objects.filter(
                content_type=userfavorite_ct
            )
        )
        
        # Conversation permissions (add, change, delete, view)
        regular_user_permissions.extend(
            Permission.objects.filter(
                content_type=conversation_ct
            )
        )
        
        # Message permissions (add, change, delete, view)
        regular_user_permissions.extend(
            Permission.objects.filter(
                content_type=message_ct
            )
        )
        
        # Favorite Prompt permissions (add, change, delete, view)
        regular_user_permissions.extend(
            Permission.objects.filter(
                content_type=favoriteprompt_ct
            )
        )
        
        # Shared Chat permissions (add, change, delete, view)
        regular_user_permissions.extend(
            Permission.objects.filter(
                content_type=sharedchat_ct
            )
        )
        
        regular_user_group.permissions.set(regular_user_permissions)
        self.stdout.write(self.style.SUCCESS(
            f'Added {len(regular_user_permissions)} permissions to Regular Users group'
        ))

        self.stdout.write(self.style.SUCCESS('Successfully set up user groups with permissions')) 
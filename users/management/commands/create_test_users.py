from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users for each group'

    def handle(self, *args, **options):
        # Create test users for each group
        self.create_content_manager()
        self.create_regular_user()
        
        self.stdout.write(self.style.SUCCESS('Successfully created test users'))
        
    def create_content_manager(self):
        username = 'content_manager'
        email = 'content@example.com'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password='contentpass',
            is_staff=True,  # Needs staff status to access admin
            first_name='Content'
        )
        
        try:
            group = Group.objects.get(name='Content Managers')
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'Added {username} to Content Managers group'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.WARNING('Content Managers group does not exist'))
            
        self.stdout.write(self.style.SUCCESS(f'Created Content Manager: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS('Password: contentpass'))
        
    def create_regular_user(self):
        username = 'user'
        email = 'user@example.com'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password='userpass',
            is_staff=False,  # Regular users don't need admin access
            first_name='Regular'
        )
        
        try:
            group = Group.objects.get(name='Regular Users')
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'Added {username} to Regular Users group'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.WARNING('Regular Users group does not exist'))
            
        self.stdout.write(self.style.SUCCESS(f'Created Regular User: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS('Password: userpass')) 
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Create an admin user for testing'

    def handle(self, *args, **options):
        # Check if admin user already exists
        username = 'admin'
        email = 'admin@example.com'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return
            
        # Create admin user
        admin_user = User.objects.create_user(
            username=username,
            email=email,
            password='adminpassword',
            is_staff=True,
            is_superuser=True,
            first_name='Admin'
        )
        
        # Add to Administrators group if it exists
        try:
            admin_group = Group.objects.get(name='Administrators')
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'Added {username} to Administrators group'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.WARNING('Administrators group does not exist'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
        self.stdout.write(self.style.SUCCESS('Password: adminpassword')) 
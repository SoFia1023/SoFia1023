from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from django.http import JsonResponse, HttpResponse, HttpRequest
from typing import Dict, Any, List, cast

# Import the is_admin function from views.py
def is_admin(user: Any) -> bool:
    """Check if the user is an admin or superuser."""
    # Type checking: ensure user is a CustomUser with the expected attributes
    if not hasattr(user, 'is_superuser') or not hasattr(user, 'groups'):
        return False
    return user.is_superuser or user.groups.filter(name='Administrators').exists()

@user_passes_test(is_admin)
def check_user_permissions(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    Admin view to check a user's permissions.
    Only accessible to superusers and members of the Administrators group.
    """
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
        
        # Get all permissions
        all_permissions = Permission.objects.all()
        
        # Get user's permissions (both direct and from groups)
        user_permissions = set()
        
        # Direct permissions - using cast to help mypy understand this is a CustomUser
        from users.models import CustomUser
        custom_user = cast(CustomUser, user)
        
        for perm in custom_user.user_permissions.all():
            user_permissions.add(f"{perm.content_type.app_label}.{perm.codename}")
        
        # Group permissions
        for group in custom_user.groups.all():
            for perm in group.permissions.all():
                user_permissions.add(f"{perm.content_type.app_label}.{perm.codename}")
        
        # Organize permissions by app and model
        permissions_by_app: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
        for perm in all_permissions:
            app_label = perm.content_type.app_label
            model_name = perm.content_type.model
            
            if app_label not in permissions_by_app:
                permissions_by_app[app_label] = {}
            
            if model_name not in permissions_by_app[app_label]:
                permissions_by_app[app_label][model_name] = []
            
            perm_key = f"{app_label}.{perm.codename}"
            permissions_by_app[app_label][model_name].append({
                'name': perm.name,
                'codename': perm.codename,
                'has_perm': perm_key in user_permissions
            })
        
        # Get user's groups
        groups = [group.name for group in user.groups.all()]
        
        context = {
            'user': user,
            'permissions_by_app': permissions_by_app,
            'groups': groups,
        }
        
        return render(request, 'admin/users/check_permissions.html', context)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

from django.urls import path, URLPattern, URLResolver
from typing import List, Union
from .views import profile, user_login, user_logout, register, check_user_permissions

app_name = 'users'


# Type hint for URL patterns
urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('admin/check-permissions/<int:user_id>/', check_user_permissions, name='check_user_permissions'),
]


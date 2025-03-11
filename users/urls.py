from typing import List, Union
from django.urls import path, URLPattern, URLResolver
from .views.auth import login_view, logout_view, register
from .views.profile import profile_view, update_profile, change_password
from .views.dashboard import dashboard

app_name = 'users'


# Type hint for URL patterns
urlpatterns: List[Union[URLPattern, URLResolver]] = [
    # Authentication URLs
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    
    # Profile URLs
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    
    # Dashboard URL
    path('dashboard/', dashboard, name='dashboard'),
]


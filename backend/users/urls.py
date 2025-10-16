from django.urls import path
from .views import (
    UserRegistrationView, login_view, logout_view, 
    UserProfileView, user_dashboard
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', login_view, name='user-login'),
    path('logout/', logout_view, name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('dashboard/', user_dashboard, name='user-dashboard'),
]
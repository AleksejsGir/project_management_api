from django.urls import path
from . import views

# Authentication endpoints following the technical requirements
urlpatterns = [
    # Core authentication endpoints (from technical requirements)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Additional user management endpoints
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile-update'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('verify-token/', views.verify_token_view, name='verify-token'),
]
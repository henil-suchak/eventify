from django.urls import path
from . import views  # Import views correctly
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),  # User registration
    path("", views.login_view, name="login"),  # Custom login view
    path("logout/", views.logout_view, name="logout"),  # Logs out user and redirects to login
    # path("profile/", views.profile_view, name="profile"),  # User profile page
    # path("update-profile/", views.update_profile_view, name="update_profile"),  # User profile update
]
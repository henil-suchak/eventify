from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Custom Sign-up Form with Profile Picture Support"""
    class Meta:
        model = CustomUser
        fields = ["name", "email", "phone_number", "profile_picture", "password1", "password2"]  # ✅ Added profile_picture
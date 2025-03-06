

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from user1.models import CustomUser
from .forms import CustomUserCreationForm  # Assuming you have an update form

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from user1.models import CustomUser
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)  # ✅ Ensure `request.FILES` is included
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("event:home")  # Redirect to homepage or dashboard
    else:
        form = CustomUserCreationForm()
    
    return render(request, "user1/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("event:home")  # Make sure "event_list" is a valid URL name
    else:
        form = AuthenticationForm()
    
    return render(request, "user1/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout


# def profile_view(request):
#     if not request.user.is_authenticated:
#         return redirect("login")  # Redirect if not logged in
    
#     return render(request, "user1/profile.html", {"user": request.user})

# def update_profile_view(request):
#     if not request.user.is_authenticated:
#         return redirect("login")
    
#     if request.method == "POST":
#         form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect("profile")  # Redirect to updated profile
#     else:
#         form = CustomUserUpdateForm(instance=request.user)
    
#     return render(request, "user1/update_profile.html", {"form": form})





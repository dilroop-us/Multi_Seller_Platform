from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm, EditProfileForm
from .models import User, UserProfile
from django.contrib import messages
from django.views.decorators.cache import never_cache


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'User account has been created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')


@login_required
@never_cache
def profile_view(request, pk):
    profile = UserProfile.objects.get(user_id=pk)
    messages.success(request, 'You have been logged in successfully!')
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
@never_cache
def edit_profile(request, pk):
    profile = UserProfile.objects.get(user_id=pk)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})

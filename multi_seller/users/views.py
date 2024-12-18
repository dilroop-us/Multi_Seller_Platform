from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, LoginForm
from .models import User, UserProfile
from django.contrib import messages
from django.views.decorators.cache import never_cache


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated user profile
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
    return redirect('login')


@login_required
@never_cache
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

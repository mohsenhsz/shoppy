from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterationForm
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in successfully', 'success')
                return redirect('shop:home')
            else:
                messages.error(request, 'email or password is wrong', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form':form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You loged out successfully', 'success')
    return redirect('shop:home')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(full_name=cd['name'], email=cd['email'], password=cd['password2'])
            user.save()
            login(request, user)
            messages.success(request, 'You signed up successfully', 'success')
            return redirect('shop:home')
    else:
        form = UserRegisterationForm()
    return render(request, 'accounts/register.html', {'form':form})

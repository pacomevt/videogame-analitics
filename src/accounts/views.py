from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
# Create your views here.

User = get_user_model()

def index(request):
    return render(request, 'accounts/index.html')

def register(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('users-register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('users-register')
            else :
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                login(request, user)
                return redirect('users-index')
        else:
            messages.info(request, 'Password not matching')
            return redirect('users-register')
    else :
        return render(request, 'accounts/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users-index')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('users-login')
    else :
        return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

# def profile(request):
#     return render(request, 'accounts/profile.html')
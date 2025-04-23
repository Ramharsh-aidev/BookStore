# accounts/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages # For displaying feedback

class RegistrationView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        # Manual form handling
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Manual Validation
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/register.html', {'username': username, 'email': email})
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html', {'username': username, 'email': email})
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/register.html', {'email': email})
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html', {'username': username})

        # Create user if validation passes
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            # Optional: Log the user in immediately after registration
            login(request, user)
            messages.success(request, f'Account created successfully for {username}. You are now logged in.')
            return redirect('home') # Redirect to home page
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'accounts/register.html', {'username': username, 'email': email})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
             return redirect('home') # Already logged in
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'accounts/login.html', {'username': username})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            # Redirect to the next page if specified, otherwise home
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html', {'username': username})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.info(request, f'You have been logged out, {username}.')
        return redirect('home') # Redirect to home after logout
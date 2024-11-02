from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect('home')
    
    return render(request, 'accounts/logout.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Pass POST data to the form
        if form.is_valid():
            # Get the cleaned data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                messages.success(request, "Login successful.")
                return redirect('home')  # Redirect to the home page or dashboard
            else:
                messages.error(request, "Invalid username or password.")  # Handle invalid login
    else:
        form = AuthenticationForm()  # Create an empty form for GET requests
    
    return render(request, 'accounts/login.html', {'form': form})

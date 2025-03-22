from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and redirect to dashboard page.
            login(request, new_user)
            return redirect('users:dashboard')  # ✅ Redirect to dashboard

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def custom_login(request):
    """Custom login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('users:dashboard')  # ✅ Redirect to dashboard
        else:
            messages.error(request, "Invalid username or password.")  # Show error message

    return render(request, 'registration/login.html')

def log_out(request):
    """Log the user out and redirect to login page."""
    logout(request)
    return redirect('users:login')  # ✅ Fix: Redirect to login page after logout

@login_required
def dashboard(request):
    """Landing page after login"""
    context = {
        'current_date': datetime.now().strftime('%B %d, %Y'),  # Format as "March 20, 2025"
        'total_sales': 0,  # Default to 0
        'pending_claims': 0,  # Default to 0
        'upcoming_inspections': 0,  # Default to 0
        'inspections': [],  # Pass an empty list for now
    }
    return render(request, 'users/dashboard.html', context)


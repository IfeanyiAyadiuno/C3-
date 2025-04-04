from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from datetime import datetime
from warranty.forms import DealerClaimForm


def register(request):
    """Register a new user (client-side only)."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('users:dashboard')  # Clients only

    context = {'form': form, 'hide_nav': True}
    return render(request, 'registration/register.html', context)


def custom_login(request):
    """Client login view. Blocks dealer-only accounts but allows superusers."""
    next_page = request.GET.get('next', '')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Block dealer-only users from logging in here
            if hasattr(user, 'is_dealer') and user.is_dealer and not user.is_superuser:
                messages.error(request, "Please log in through the dealership portal.")
                return redirect('users:dealer_login')

            login(request, user)
            return redirect('users:dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'registration/login.html', {'hide_nav': True})



def dealer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('users:dealer_dashboard')
            else:
                return render(request, 'registration/access_denied.html', {
                    'message': 'You do not have access to the dealership portal.'
                })
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'registration/dealer_login.html', {'hide_nav': True})



def log_out(request):
    """Log the user out and redirect to login page."""
    logout(request)
    return redirect('users:login')


@login_required
def dashboard(request):
    """Landing page for client users after login."""
    context = {
        'current_date': datetime.now().strftime('%B %d, %Y'),
        'total_sales': 0,
        'pending_claims': 0,
        'upcoming_inspections': 0,
        'inspections': [],
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def dealer_dashboard(request):
    """Landing page for dealership users."""
    context = {
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    return render(request, 'users/dealer_dashboard.html', context)


@login_required
def record_sale(request):
    current_date = datetime.now().strftime('%B %d, %Y')
    return render(request, 'users/record_sale.html', {'current_date': current_date})


@login_required
def submit_claim(request):
    """Handles the dealer warranty claim form submission."""
    if request.method == 'POST':
        form = DealerClaimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:dealer_dashboard')
    else:
        form = DealerClaimForm()

    return render(request, 'users/submit_claim.html', {
        'form': form,
        'current_date': datetime.now().strftime('%B %d, %Y'),
    })









"""
Authentication Views for Museum Staff
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from core.forms import MuseumRegistrationForm, StaffRegistrationForm, StaffLoginForm
from core.models import Museum, MuseumStaff


def register_view(request):
    """Combined registration view for museum and staff"""
    if request.method == 'POST':
        museum_form = MuseumRegistrationForm(request.POST, request.FILES)
        staff_form = StaffRegistrationForm(request.POST)
        
        if museum_form.is_valid() and staff_form.is_valid():
            try:
                with transaction.atomic():
                    # Create museum
                    museum = museum_form.save()
                    
                    # Create staff account
                    staff = staff_form.save(commit=False)
                    staff.museum = museum
                    staff.role = 'admin'  # First user is admin
                    staff.save()
                    
                    # Log the user in
                    login(request, staff)
                    messages.success(request, f'Welcome to ArtScope, {staff.get_full_name()}!')
                    return redirect('dashboard')  # You'll need to create this view
                    
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        museum_form = MuseumRegistrationForm()
        staff_form = StaffRegistrationForm()
    
    return render(request, 'auth/register.html', {
        'museum_form': museum_form,
        'staff_form': staff_form,
    })


def login_view(request):
    """Login view for museum staff"""
    if request.method == 'POST':
        form = StaffLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = StaffLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')


@login_required
def dashboard_view(request):
    """Dashboard for logged-in museum staff"""
    museum = request.user.museum
    artworks = museum.artworks.all()[:10]
    
    context = {
        'museum': museum,
        'artworks': artworks,
        'total_artworks': museum.artworks.count(),
        'active_artworks': museum.artworks.filter(is_on_display=True).count(),
    }
    
    return render(request, 'dashboard.html', context)

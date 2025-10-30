from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import StudentUser
from django.core.mail import send_mail
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next')
        # authenticate() expects the Django username field; we now read 'username' from the form
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # If a next parameter was provided (e.g., by @user_passes_test redirect), honor it
            if next_url:
                return redirect(next_url)
            return redirect('landing_page')
        else:
            messages.error(request, 'Invalid email or password.')
            
    # Pass through 'next' if present so the template can include it in the POST
    context = {'next': request.GET.get('next', '')}
    return render(request, 'authentication/login.html', context)

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        roll_number = request.POST.get('roll_number')
        room_number = request.POST.get('room_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate password
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/register.html')
            
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'authentication/register.html')
        
        # check if a Django User with this email/username exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'authentication/register.html')

        # check for existing student_id in profile
        if StudentUser.objects.filter(student_id=roll_number).exists():
            messages.error(request, 'Roll number already registered.')
            return render(request, 'authentication/register.html')
        
        # Create user and profile
        try:
            # create Django auth user (use email as username)
            user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name)

            # create student profile with default hostel type
            StudentUser.objects.create(
                user=user,
                student_id=roll_number,
                room_number=room_number,
                hostel_type='B',  # Default to Boys hostel
                contact_number=''
            )
            
            # Send welcome email
            send_mail(
                'Welcome to Hostel Query System',
                f'Hello {full_name},\n\nYour account has been created successfully.\n\n'
                f'You can now login with your email: {email}\n\n'
                'Best regards,\nHostel Query System Team',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Registration successful. Please check your email for login credentials.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'authentication/register.html')
            
    return render(request, 'authentication/register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

def signup_view(request):
    password_did_not_match = None
    email_already_exists = None
    atleast_8_characters = None
    numeric = None

    if request.method == 'POST':
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        if not csrf_token:
            return HttpResponseForbidden("CSRF token missing")
        
        # Retrieve form data
        full_name = request.POST.get('full_name')  # New field
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profession = request.POST.get('profession')  # New field

        CustomUser = get_user_model()

        e1 = e2 = e3 = e4 = False
        # Validate that passwords match
        if password1 != password2:
            password_did_not_match = "Passwords did not match"
            e1 = True
        if CustomUser.objects.filter(email=email).exists():
            email_already_exists = "Email already exists"
            e2 = True
        if len(password1) < 8:
            atleast_8_characters = "Your password must contain at least 8 characters."
            e3 = True
        if password1.isdigit():
            numeric = "Your password can’t be entirely numeric."
            e4 = True
        if not (e1 or e2 or e3 or e4):
            # Create user with all attributes
            user = CustomUser.objects.create_user(
                email=email,
                password=password1,
                full_name=full_name,  # Storing full name
                profession=profession  # Storing profession
            )
            
            # Log the user in
            login(request, user)
            
            if user.profession == 'student':
                return redirect('edu:student_dashboard')
            elif user.profession == 'teacher':
                return redirect('edu:teacher_dashboard')

    return render(request, 'accounts/register.html', {
        'password_did_not_match': password_did_not_match,
        'email_already_exists': email_already_exists,
        'atleast_8_characters': atleast_8_characters,
        'numeric': numeric
    })

def login_view(request):
    error_message = None
    if request.method == 'POST':
        # Validate CSRF token
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        if not csrf_token:
            return HttpResponseForbidden("CSRF token missing")
        
        # Process form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Login the user
            login(request, user)            
            if user.profession == 'student':
                return redirect('edu:student_dashboard')
            elif user.profession == 'teacher':
                return redirect('edu:teacher_dashboard')
        else:
            # Authentication failed
            error_message = "Invalid email or password. Please try again."
    
    # If the request method is GET or authentication fails, render the login template
    return render(request, 'accounts/login.html',{'error_message': error_message})       

def logout_view(request):
    # Logout the user
    logout(request)
    return redirect('accounts:login')
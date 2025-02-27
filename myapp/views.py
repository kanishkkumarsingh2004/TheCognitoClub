from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django import forms
from dotenv import load_dotenv
from .models import Event, UserProfile, Registration, RegistrationSettings
from .forms import RegistrationForm, CustomLoginForm
from django.http import JsonResponse
import os
load_dotenv()
def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'mobile')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if UserProfile.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})

def home(request):
    return render(request, 'myapp/home.html')

def contact(request):
    return render(request, 'myapp/contact.html')

def collaboration(request):
    return render(request, 'myapp/collaboration.html')

def about(request):
    return render(request, 'myapp/about.html')

@login_required
def dashboard(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile': user_profile.mobile,  
        }
    except UserProfile.DoesNotExist:
        context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile': 'N/A', 
        }
    return render(request, 'myapp/dashboard.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()

                UserProfile.objects.create(user=user, mobile=form.cleaned_data['mobile'])
                login(request, user)
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'myapp/signup.html', {'form': form})
        else:
            return render(request, 'myapp/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            send_mail(
                subject=f"New Contact Message from {name}",
                message=f"Name: {name}\n\nEmail: {email}\n\n\n\nMessage: {message}",
                from_email=email,
                recipient_list=[os.getenv('EMAIL')],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")

    return render(request, "myapp/contact.html")


def terms_of_service(request):
    return render(request, 'myapp/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'myapp/privacy_policy.html')

def dashboard_view(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now())
    context = {
        'upcoming_events': upcoming_events
    }
    return render(request, 'myapp/dashboard.html', context)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create and save Registration instance
                registration = Registration(
                    full_name=form.cleaned_data['full_name'],
                    usn=form.cleaned_data['usn'],
                    branch=form.cleaned_data['branch'],
                    email=form.cleaned_data['email'],
                    mobile_number=form.cleaned_data['mobile_number'],
                    domains=', '.join(form.cleaned_data['domains']),  
                    superpower=', '.join(form.cleaned_data['superpower']),
                    interests=', '.join(form.cleaned_data['interests']), 
                )
                registration.save()
                messages.success(request, 'Registration successful!')
                return redirect('success')  # Redirect to success page
            except Exception as e:
                messages.error(request, f'Error saving registration: {str(e)}')
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')
    else:
        form = RegistrationForm()
    
    return render(request, 'myapp/register.html', {'form': form})

def success(request):
    return render(request, 'myapp/success.html')
def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    context = {
        'upcoming_events': upcoming_events
    }
    return render(request, 'myapp/home.html', context)








def get_registration_deadline(request):
    try:
        settings = RegistrationSettings.objects.first()
        if settings:
            return JsonResponse({
                'deadline': settings.registration_deadline.isoformat()
            })
        return JsonResponse({'error': 'No deadline set'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
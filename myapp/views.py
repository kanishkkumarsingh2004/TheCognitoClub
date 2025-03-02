from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django import forms
from dotenv import load_dotenv
from .models import Event, UserProfile, Registration, RegistrationSettings, Challenge, ChallengeParticipation
from .forms import RegistrationForm, CustomLoginForm
from django.http import JsonResponse
import os
from django.db import IntegrityError

load_dotenv()
def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=15, required=True)
    usn = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'mobile', 'usn')
    
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
       
    def clean_usn(self):
        usn = self.cleaned_data.get('usn')
        if UserProfile.objects.filter(usn=usn).exists():
            raise forms.ValidationError("This USN is already registered.")
        return usn
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    context = {
        'upcoming_events': upcoming_events
    }
    return render(request, 'myapp/home.html', context)


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

def collaboration(request):
    return render(request, 'myapp/collaboration.html')

def about(request):
    return render(request, 'myapp/about.html')

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------



@login_required
def resources(request):
    return render(request, 'myapp/resources.html')

@login_required
def leaderboard_view(request):
    # Get all user profiles ordered by points
    leaderboard = UserProfile.objects.select_related('user').order_by('-points')[:10]
    
    # Add rank to each user
    ranked_leaderboard = []
    for rank, profile in enumerate(leaderboard, start=1):
        ranked_leaderboard.append({
            'rank': rank,
            'user': profile.user,
            'points': profile.points
        })
    
    return render(request, 'myapp/leaderboard.html', {
        'leaderboard': ranked_leaderboard
    })

@login_required
def challenges_view(request):
    active_challenges = Challenge.objects.filter(end_date__gte=timezone.now())
    return render(request, 'myapp/challenges.html', {'challenges': active_challenges})

@login_required
def join_challenge(request, challenge_id):
    if request.method == 'POST':
        challenge = get_object_or_404(Challenge, id=challenge_id)
        user = request.user
        
        try:
            user_profile = UserProfile.objects.get(user=user)
            ChallengeParticipation.objects.create(
                user=user,
                challenge=challenge,
                usn=user_profile.usn,
                mobile=user_profile.mobile
            )
            return redirect('challenge_join_success')
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile not found. Please complete your profile.")
            return redirect('dashboard')

def challenge_join_success(request):
    return render(request, 'myapp/challenge_join_success.html')

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
            'usn': user_profile.usn,  
        }
    except UserProfile.DoesNotExist:
        context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile': 'N/A',
            'usn': 'N/A',
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

                UserProfile.objects.create(user=user,
                                            mobile=form.cleaned_data['mobile'],
                                            usn=form.cleaned_data['usn']
                                        )
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
                return redirect('success')
            except Exception as e:
                messages.error(request, f'Error saving registration: {str(e)}')
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')
    else:
        form = RegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})

def success(request):
    return render(request, 'myapp/success.html')


def challenges_view(request):
    challenges = Challenge.objects.filter(end_date__gte=timezone.now())
    return render(request, 'myapp/challenges.html', {'challenges': challenges})

@login_required
def submit_challenge(request, challenge_id):
    if request.method == 'POST':
        challenge = get_object_or_404(Challenge, id=challenge_id)
        participation = get_object_or_404(
            ChallengeParticipation,
            user=request.user,
            challenge=challenge
        )
        submission_url = request.POST.get('submission_url')
        if submission_url:
            participation.submission_url = submission_url
            participation.submission_status = 'submitted'
            participation.save()
            messages.success(request, 'Your submission has been recorded!')
        else:
            messages.error(request, 'Please provide a valid submission URL')
    return redirect('challenge_detail', challenge_id=challenge_id)

def challenge_detail_view(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    has_joined = False
    submission_status = None
    review_notes = None
    submission_url = None
    points = challenge.points if challenge else 0
    
    if request.user.is_authenticated:
        participation = ChallengeParticipation.objects.filter(
            user=request.user,
            challenge=challenge
        ).first()
        if participation:
            has_joined = True
            submission_status = participation.get_submission_status_display()
            review_notes = participation.review_notes
            submission_url = participation.submission_url
    
    return render(request, 'myapp/challenge_detail.html', {
        'challenge': challenge,
        'has_joined': has_joined,
        'submission_status': submission_status,
        'review_notes': review_notes,
        'submission_url': submission_url,
        'points': points
    })

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

@login_required
def join_challenge(request, challenge_id):
    if request.method == 'POST':
        challenge = get_object_or_404(Challenge, id=challenge_id)
        user = request.user
        
        try:
            user_profile = UserProfile.objects.get(user=user)
            
            ChallengeParticipation.objects.create(
                user=user,
                challenge=challenge,
                usn=user_profile.usn,
                mobile=user_profile.mobile
            )
            return redirect('challenge_join_success')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found. Please complete your profile.')
        except IntegrityError:
            messages.warning(request, 'You have already joined this challenge.')
        except Exception as e:
            messages.error(request, f'Error joining challenge: {str(e)}')
        
        return redirect('challenge_detail', challenge_id=challenge_id)
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import join_challenge, challenge_join_success

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('collaboration/', views.collaboration, name='collaboration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('get-registration-deadline/', views.get_registration_deadline, name='get-registration-deadline'),
    path('resources/', views.resources, name='resources'),
    path('leaderboard/', (views.leaderboard_view), name='leaderboard'),
    path('challenges/', views.challenges_view, name='challenges'),
    path('challenges/<int:challenge_id>/', views.challenge_detail_view, name='challenge_detail'),
    path('challenge/join/<int:challenge_id>/', join_challenge, name='join_challenge'),
    path('challenge/join/success/', challenge_join_success, name='challenge_join_success'),
    path('challenge/submit/<int:challenge_id>/', views.submit_challenge, name='submit_challenge'),

]
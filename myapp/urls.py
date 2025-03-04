from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

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
    path('challenge/join/<int:challenge_id>/', views.join_challenge, name='join_challenge'),
    path('challenge/join/success/', views.challenge_join_success, name='challenge_join_success'),
    path('challenge/submit/<int:challenge_id>/', views.submit_challenge, name='submit_challenge'),
    # password reset links
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
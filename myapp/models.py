from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django_ckeditor_5.fields import CKEditor5Field

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=200, default='Jain (Deemed-to-be University)')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['date']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, unique=True)
    usn = models.CharField(max_length=20, unique=True) 
    points = models.PositiveIntegerField(default=0) 
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.mobile})"
    
    def save(self, *args, **kwargs):
        # Ensure USN is stored in uppercase
        self.usn = self.usn.upper()
        super().save(*args, **kwargs)

class Registration(models.Model):
    full_name = models.CharField(max_length=100000)
    usn = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10)
    domains = models.CharField(max_length=2000)
    superpower = models.CharField(max_length=500000)
    interests = models.CharField(max_length=500000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        # Ensure USN is stored in uppercase
        self.usn = self.usn.upper()
        super().save(*args, **kwargs)
    

class RegistrationSettings(models.Model):
    registration_deadline = models.DateTimeField()
    
    def __str__(self):
        return f"Registration Settings (Deadline: {self.registration_deadline})"
    
    class Meta:
        verbose_name_plural = "Registration Settings"



class Challenge(models.Model):
    title = models.CharField(max_length=20000)
    description = CKEditor5Field('Description', config_name='default')
    points = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    technology_stack = CKEditor5Field('Technology Stack', config_name='default', blank=True)
    requirements = CKEditor5Field('Requirements', config_name='default', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ChallengeParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    usn = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)
    start_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    submission_url = models.URLField(blank=True, null=True)
    submission_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('submitted', 'Submitted'),
            ('reviewed', 'Reviewed'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    review_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"
    
    def save(self, *args, **kwargs):
        # Ensure USN is stored in uppercase
        self.usn = self.usn.upper()
        super().save(*args, **kwargs)
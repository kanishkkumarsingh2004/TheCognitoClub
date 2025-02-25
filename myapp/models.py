from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User


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
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.mobile})"

class Registration(models.Model):
    full_name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20)
    branch = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10)
    domains = models.CharField(max_length=200)
    about_yourself = models.CharField(max_length=50)
    superpower = models.CharField(max_length=500)
    interests = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
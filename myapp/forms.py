from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100000)
    usn = forms.CharField(max_length=10, min_length=10)
    branch = forms.CharField(max_length=50)
    email = forms.CharField()
    mobile_number = forms.CharField(max_length=10, min_length=10)
    domains = forms.MultipleChoiceField(
        choices=[
            ('design', 'Design'),
            ('tech', 'Tech'),
            ('event_management', 'Event Management'),
            ('social_media', 'Social Media'),
            ('coordinators', 'Coordinators'),
            ('Outreach_and_Marketing', 'Outreach and Marketing'),
        ],
        widget=forms.CheckboxSelectMultiple
    )
    superpower = forms.MultipleChoiceField(
        choices=[
            ('tech_guru', 'Destech_guruign'),
            ('public_speaking', 'public_speaking'),
            ('design_wizard', 'design_wizard'),
            ('the_fixer', 'the_fixer'),
            ('mastermind', 'mastermind'),
        ],
        widget=forms.CheckboxSelectMultiple
    )
    interests = forms.MultipleChoiceField(
    choices=[
        ('ai_ml', 'AI & ML'),
        ('devops_cloud', 'DevOps & Cloud'),
        ('cybersecurity', 'Cybersecurity'),
        ('web_app_dev', 'Web/App Dev'),
        ('data_science', 'Data Science'),
        ('competitive_coding', 'Competitive Coding'),
        ('event_management', 'Event Management'),
        ('content_creation', 'Content Creation'),
        ('graphic_design', 'Graphic Design'),
        ('other', 'Other'),
    ],
    widget=forms.CheckboxSelectMultiple
    )




class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username']
        self.fields['password']
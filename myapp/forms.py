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


class DynamicEventRegistrationForm(forms.Form):
    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add fields dynamically based on event configuration
        for field_config in event.form_fields.all():
            field_kwargs = {
                'required': field_config.required,
                'label': field_config.field_name
            }
            
            if field_config.max_length:
                field_kwargs['max_length'] = field_config.max_length
            if field_config.min_length:
                field_kwargs['min_length'] = field_config.min_length

            if field_config.field_type == 'text':
                self.fields[field_config.field_name] = forms.CharField(**field_kwargs)
            elif field_config.field_type == 'number':
                self.fields[field_config.field_name] = forms.IntegerField(**field_kwargs)
            elif field_config.field_type == 'email':
                self.fields[field_config.field_name] = forms.EmailField(**field_kwargs)
            elif field_config.field_type == 'tel':
                self.fields[field_config.field_name] = forms.CharField(**field_kwargs)
            elif field_config.field_type == 'team':
                field_kwargs['max_length'] = 3
                field_kwargs['min_length'] = 1
                self.fields[field_config.field_name] = forms.CharField(**field_kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # Convert USN to uppercase if present
        if 'usn' in cleaned_data:
            cleaned_data['usn'] = cleaned_data['usn'].upper()
        return cleaned_data
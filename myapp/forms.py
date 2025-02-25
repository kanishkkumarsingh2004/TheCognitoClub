from django import forms

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    usn = forms.CharField(max_length=20, required=True)
    branch = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(max_length=10, min_length=10, required=True)
    domains = forms.MultipleChoiceField(
        choices=[
            ('design', 'Design'),
            ('tech', 'Tech'),
            ('event_management', 'Event Management'),
            ('social_media', 'Social Media'),
            ('coordinators', 'Coordinators'),
            ('Outreach_and_Marketing', 'Outreach and Marketing'),
        ],
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    about_yourself = forms.CharField(max_length=500, required=True, help_text="Use 5 words only.")



class CustomLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
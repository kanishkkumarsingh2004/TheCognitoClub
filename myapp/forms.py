from django import forms

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    usn = forms.CharField(max_length=10, min_length=10, required=True)
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
    superpower = forms.MultipleChoiceField(
        choices=[
            ('tech_guru', 'Destech_guruign'),
            ('public_speaking', 'public_speaking'),
            ('design_wizard', 'design_wizard'),
            ('the_fixer', 'the_fixer'),
            ('mastermind', 'mastermind'),
        ],
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    excites = forms.MultipleChoiceField(
        choices=[
            ('ai_ml', 'ai_ml'),
            ('devops_cloud', 'devops_cloud'),
            ('cybersecurity', 'cybersecurity'),
            ('theweb_app_dev_fixer', 'theweb_app_dev_fixer'),
            ('data_science', 'data_science'),
            ('competitive_coding', 'competitive_coding'),
            ('event_management', 'event_management'),
            ('content_creation', 'content_creation'),
            ('graphic_design', 'graphic_design'),
            ('other', 'other'),

        ],
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    about_yourself = forms.CharField(max_length=5000000, required=True)



class CustomLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
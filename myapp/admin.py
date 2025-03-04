from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Event, UserProfile, RegistrationSettings, Registration, Challenge, ChallengeParticipation, EventFormField
from django.http import HttpResponse
import csv
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms


class EventFormFieldInline(admin.TabularInline):
    model = EventFormField
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventFormFieldInline]
    list_display = ('title', 'date', 'venue', 'created_at')
    search_fields = ('title', 'description')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'
    fields = ('mobile','usn')


class UserChallengeParticipationInline(admin.TabularInline):
    model = ChallengeParticipation
    extra = 0
    raw_id_fields = ('challenge',)
    readonly_fields = ('usn', 'mobile', 'start_date')


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_mobile', 'get_usn') 
    list_select_related = ('userprofile',)

    def get_mobile(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.mobile
        return 'N/A'
    get_mobile.short_description = 'Mobile'

    def get_usn(self, obj):  # Add this method
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.usn
        return 'N/A'
    get_usn.short_description = 'USN'  # Set column header

# Unregister the default User admin
admin.site.unregister(User)
# Register the User model with the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Full Name', 'USN', 'Branch', 'Email', 'Mobile Number', 'Domains', 'Created At', 'Intrest', 'Superpower'])
    
    for obj in queryset:
        writer.writerow([
            obj.full_name,
            obj.usn,
            obj.branch,
            obj.email,
            obj.mobile_number,
            obj.domains,
            obj.created_at,
            obj.interests,
            obj.superpower,
        ])
    
    return response
export_to_csv.short_description = "Export selected registrations to CSV"

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'usn', 'branch', 'email', 'mobile_number', 'created_at')
    search_fields = ('full_name', 'usn', 'branch', 'email', 'mobile_number')
    actions = [export_to_csv]

@admin.register(RegistrationSettings)
class RegistrationSettingsAdmin(admin.ModelAdmin):
    list_display = ('registration_deadline',)

class ChallengeForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditor5Widget(config_name='default'))
    
    class Meta:
        model = Challenge
        fields = '__all__'


class ChallengeParticipationInline(admin.TabularInline):
    model = ChallengeParticipation
    extra = 0
    raw_id_fields = ('user',)
    readonly_fields = ('usn', 'mobile', 'start_date')


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeForm
    list_display = ('title', 'points', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')
    inlines = [ChallengeParticipationInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'points')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Details', {
            'fields': ('technology_stack', 'requirements'),
            'classes': ('collapse',)
        }),
    )
@admin.register(ChallengeParticipation)
class ChallengeParticipationAdmin(admin.ModelAdmin):
    list_display = ('usn', 'get_full_name', 'user', 'mobile', 'challenge', 'submission_url', 'submission_status', 'review_notes', 'start_date')
    list_filter = ('challenge', 'start_date', 'submission_status')
    search_fields = ('user__username', 'usn', 'mobile', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user', 'challenge')
    date_hierarchy = 'start_date'
    list_editable = ('submission_status', 'review_notes')
    fieldsets = (
        (None, {
            'fields': ('user', 'challenge', 'usn', 'mobile')
        }),
        ('Submission Details', {
            'fields': ('submission_url', 'submission_status', 'review_notes')
        }),
    )

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__first_name'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.submission_status == 'approved':
            # Update user points when submission is approved
            user_profile = UserProfile.objects.get(user=obj.user)
            user_profile.points += obj.challenge.points
            user_profile.save()

@admin.register(UserProfile)
class UserAchievedPointsAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'usn', 'mobile', 'points')  # Display full name instead of user
    list_editable = ('points',)  # Make points editable directly in list view
    search_fields = ('user__username', 'usn', 'mobile', 'user__first_name', 'user__last_name')  # Add search functionality
    # list_filter = ('points',)  # Add filter by points

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__first_name'
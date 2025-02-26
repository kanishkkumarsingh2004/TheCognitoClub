from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Event, UserProfile, RegistrationSettings

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'venue', 'created_at')
    search_fields = ('title', 'description')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'
    fields = ('mobile',)

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_mobile')
    list_select_related = ('userprofile',)

    def get_mobile(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.mobile
        return 'N/A'
    get_mobile.short_description = 'Mobile'

# Unregister the default User admin
admin.site.unregister(User)
# Register the User model with the custom UserAdmin
admin.site.register(User, CustomUserAdmin)



import csv
from django.http import HttpResponse
from .models import Registration

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Full Name', 'USN', 'Branch', 'Email', 'Mobile Number', 'Domains', 'About Yourself', 'Created At', 'Intrest', 'Superpower'])
    
    for obj in queryset:
        writer.writerow([
            obj.full_name,
            obj.usn,
            obj.branch,
            obj.email,
            obj.mobile_number,
            obj.domains,
            obj.about_yourself,
            obj.created_at,
            obj.intrest,
            obj.superpower,
        ])
    
    return response
export_to_csv.short_description = "Export selected registrations to CSV"

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'usn', 'branch', 'email', 'mobile_number', 'created_at')
    actions = [export_to_csv]



@admin.register(RegistrationSettings)
class RegistrationSettingsAdmin(admin.ModelAdmin):
    list_display = ('registration_deadline',)
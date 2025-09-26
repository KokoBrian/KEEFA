from django.contrib import admin
from .models import ContactInquiry, OfficeLocation, ContactPerson, SocialMediaAccount


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'status', 'priority', 'response_sent', 'created_at']
    list_filter = ['subject', 'status', 'priority', 'response_sent', 'follow_up_required', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'organization')
        }),
        ('Inquiry Details', {
            'fields': ('subject', 'message', 'subscribe_newsletter')
        }),
        ('Internal Tracking', {
            'fields': ('status', 'priority', 'assigned_to', 'internal_notes')
        }),
        ('Response Tracking', {
            'fields': ('response_sent', 'response_sent_at', 'follow_up_required', 'follow_up_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_resolved', 'mark_as_in_progress']
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')
    mark_as_resolved.short_description = "Mark selected inquiries as resolved"
    
    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Mark selected inquiries as in progress"


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'county', 'phone', 'is_main_office', 'is_public', 'order']
    list_editable = ['order', 'is_public']
    list_filter = ['is_main_office', 'is_public', 'county']
    search_fields = ['name', 'city', 'address']
    
    fieldsets = (
        ('Location Details', {
            'fields': ('name', 'address', 'city', 'county', 'postal_code', 'country')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'fax')
        }),
        ('Geographic Coordinates', {
            'fields': ('latitude', 'longitude')
        }),
        ('Office Information', {
            'fields': ('office_hours', 'services_offered')
        }),
        ('Display Settings', {
            'fields': ('is_main_office', 'is_public', 'order')
        }),
    )


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'department', 'email', 'is_public', 'order']
    list_editable = ['order', 'is_public']
    list_filter = ['department', 'is_public']
    search_fields = ['name', 'position', 'email']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'position', 'department', 'photo', 'bio')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'extension')
        }),
        ('Availability', {
            'fields': ('office_hours', 'languages_spoken')
        }),
        ('Display Settings', {
            'fields': ('is_public', 'order')
        }),
    )


@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['platform', 'username', 'follower_count', 'is_primary', 'show_in_footer', 'order']
    list_editable = ['order', 'is_primary', 'show_in_footer']
    list_filter = ['platform', 'is_primary', 'show_in_footer', 'show_in_contact']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('platform', 'username', 'url', 'follower_count')
        }),
        ('Display Settings', {
            'fields': ('is_primary', 'show_in_footer', 'show_in_contact', 'order')
        }),
    )
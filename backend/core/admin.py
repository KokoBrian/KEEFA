from django.contrib import admin
from .models import (
    Organization, ImpactStatistic, TeamMember, Partner, 
    Testimonial, FAQ, SiteSettings
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'logo')
        }),
        ('About Us', {
            'fields': ('mission', 'vision', 'values', 'story')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url')
        }),
        ('Images', {
            'fields': ('hero_image',)
        }),
    )


@admin.register(ImpactStatistic)
class ImpactStatisticAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'color', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['color', 'is_active']
    ordering = ['order']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'position']
    ordering = ['order']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partnership_type', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['partnership_type', 'is_active']
    search_fields = ['name']
    ordering = ['order']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'program_type', 'rating', 'is_featured', 'order', 'is_active']
    list_editable = ['is_featured', 'order', 'is_active']
    list_filter = ['program_type', 'rating', 'is_featured', 'is_active']
    search_fields = ['name', 'content']
    ordering = ['order']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    ordering = ['order']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['meta_title', 'maintenance_mode', 'updated_at']
    fieldsets = (
        ('General Settings', {
            'fields': ('maintenance_mode', 'maintenance_message')
        }),
        ('Contact Settings', {
            'fields': ('whatsapp_number', 'emergency_contact')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id', 'facebook_pixel_id')
        }),
    )

    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the settings
        return False
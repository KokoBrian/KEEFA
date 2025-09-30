from django.contrib import admin
from django.utils.html import format_html
from .models import DonationCampaign, Donation, DonationImpact, Volunteer, Partnership


@admin.register(DonationCampaign)
class DonationCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'campaign_type', 'goal_amount', 'raised_amount', 'progress_bar', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']
    list_filter = ['campaign_type', 'is_featured', 'is_urgent', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    
    def progress_bar(self, obj):
        percentage = obj.progress_percentage
        color = 'green' if percentage >= 75 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0;">'
            '<div style="width: {}%; background-color: {}; height: 20px; text-align: center; color: white;">'
            '{}%</div></div>',
            percentage, color, round(percentage, 1)
        )
    progress_bar.short_description = 'Progress'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_display', 'amount', 'currency', 'campaign', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'donation_type', 'is_anonymous', 'is_recurring']
    search_fields = ['donor_name', 'donor_email', 'transaction_id']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']
    
    def donor_display(self, obj):
        return "Anonymous" if obj.is_anonymous else obj.donor_name
    donor_display.short_description = 'Donor'
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'currency', 'donation_type', 'campaign', 'designation', 'message')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'transaction_id', 'payment_reference', 'status', 'processed_at')
        }),
        ('Recurring Donations', {
            'fields': ('is_recurring', 'next_payment_date', 'subscription_id')
        }),
        ('Receipt & Tax', {
            'fields': ('is_tax_deductible', 'receipt_sent', 'receipt_sent_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DonationImpact)
class DonationImpactAdmin(admin.ModelAdmin):
    list_display = ['donation', 'beneficiaries_count', 'report_date', 'report_sent']
    list_filter = ['report_sent', 'report_date']
    search_fields = ['donation__donor_name', 'impact_description']


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'location', 'status', 'hours_contributed', 'created_at']
    list_filter = ['status', 'availability', 'location']
    search_fields = ['first_name', 'last_name', 'email', 'skills_experience']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'location')
        }),
        ('Volunteer Details', {
            'fields': ('interests', 'skills_experience', 'availability')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'hours_contributed', 'projects_participated', 'start_date')
        }),
        ('Notes', {
            'fields': ('admin_notes',)
        }),
    )


@admin.register(Partnership)
class PartnershipAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'contact_person', 'organization_type', 'status', 'created_at']
    list_filter = ['organization_type', 'status']
    search_fields = ['organization_name', 'contact_person', 'email']
    
    fieldsets = (
        ('Organization Information', {
            'fields': ('organization_name', 'organization_type', 'website')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'email', 'phone')
        }),
        ('Partnership Details', {
            'fields': ('partnership_interests', 'proposal_details')
        }),
        ('Status & Follow-up', {
            'fields': ('status', 'follow_up_date', 'admin_notes')
        }),
    )
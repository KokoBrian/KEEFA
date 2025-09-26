from django.contrib import admin
from .models import (
    Program, ScholarshipApplication, WorkshopRegistration, 
    ProjectLocation, SuccessStory
)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'program_type', 'beneficiaries_count', 'is_accepting_applications', 'order', 'is_active']
    list_editable = ['order', 'is_active', 'is_accepting_applications']
    list_filter = ['program_type', 'is_accepting_applications', 'is_active']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'program_type', 'short_description', 'full_description')
        }),
        ('Visual Elements', {
            'fields': ('image', 'icon', 'color')
        }),
        ('Program Metrics', {
            'fields': ('beneficiaries_count', 'success_rate')
        }),
        ('Application Details', {
            'fields': ('eligibility_criteria', 'application_process', 'requirements')
        }),
        ('Application Status', {
            'fields': ('is_accepting_applications', 'application_deadline')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'education_level', 'status', 'created_at']
    list_filter = ['status', 'education_level', 'gender', 'county', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Address', {
            'fields': ('county', 'sub_county', 'ward', 'village')
        }),
        ('Education', {
            'fields': ('education_level', 'current_school', 'class_year', 'previous_grades')
        }),
        ('Family Information', {
            'fields': ('family_income', 'family_size', 'guardian_name', 'guardian_occupation', 'guardian_phone')
        }),
        ('Essays', {
            'fields': ('why_deserve_scholarship', 'career_goals', 'community_involvement')
        }),
        ('Documents', {
            'fields': ('academic_transcripts', 'recommendation_letter', 'financial_documents')
        }),
        ('Review', {
            'fields': ('status', 'review_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Scholarship Details', {
            'fields': ('scholarship_amount', 'scholarship_duration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WorkshopRegistration)
class WorkshopRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'workshop_type', 'completion_status', 'is_confirmed', 'created_at']
    list_filter = ['workshop_type', 'completion_status', 'is_confirmed', 'gender', 'county']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'age', 'gender')
        }),
        ('Location', {
            'fields': ('county', 'sub_county')
        }),
        ('Workshop Details', {
            'fields': ('workshop_type', 'preferred_schedule', 'expectations')
        }),
        ('Background', {
            'fields': ('education_level', 'current_occupation', 'previous_experience')
        }),
        ('Status', {
            'fields': ('is_confirmed', 'workshop_batch', 'completion_status')
        }),
    )


@admin.register(ProjectLocation)
class ProjectLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'status', 'beneficiaries_count', 'start_date', 'is_active']
    list_filter = ['status', 'county', 'is_active']
    search_fields = ['name', 'county', 'sub_county']
    
    fieldsets = (
        ('Location Details', {
            'fields': ('name', 'county', 'sub_county', 'ward')
        }),
        ('Coordinates', {
            'fields': ('latitude', 'longitude')
        }),
        ('Project Information', {
            'fields': ('project_types', 'description', 'beneficiaries_count', 'start_date', 'status')
        }),
        ('Media', {
            'fields': ('main_image', 'gallery_images')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'title', 'is_featured', 'publish_date', 'order', 'is_active']
    list_editable = ['is_featured', 'order', 'is_active']
    list_filter = ['program', 'is_featured', 'is_active', 'publish_date']
    search_fields = ['name', 'title', 'story']
    date_hierarchy = 'publish_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'program', 'title', 'story')
        }),
        ('Personal Details', {
            'fields': ('age', 'location', 'current_status', 'achievements')
        }),
        ('Media', {
            'fields': ('profile_image', 'before_image', 'after_image', 'video_url')
        }),
        ('Metrics', {
            'fields': ('impact_metrics',)
        }),
        ('Publishing', {
            'fields': ('is_featured', 'publish_date', 'order', 'is_active')
        }),
    )
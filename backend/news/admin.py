from django.contrib import admin
from .models import NewsCategory, NewsArticle, Event, EventRegistration, Newsletter


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_featured', 'is_published', 'views_count', 'publish_date']
    list_editable = ['is_featured', 'is_published']
    list_filter = ['category', 'is_featured', 'is_published', 'publish_date', 'author']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_date'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image', 'gallery_images', 'video_url')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Publishing', {
            'fields': ('author', 'publish_date', 'is_featured', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Related Content', {
            'fields': ('related_articles',)
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'venue', 'status', 'is_featured']
    list_editable = ['is_featured']
    list_filter = ['event_type', 'status', 'is_featured', 'requires_registration']
    search_fields = ['title', 'description', 'venue']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'slug', 'description', 'event_type', 'featured_image')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date')
        }),
        ('Location', {
            'fields': ('venue', 'address', 'latitude', 'longitude')
        }),
        ('Registration', {
            'fields': ('requires_registration', 'registration_deadline', 'max_participants', 'registration_fee')
        }),
        ('Contact', {
            'fields': ('contact_person', 'contact_email', 'contact_phone')
        }),
        ('Status', {
            'fields': ('status', 'is_featured')
        }),
        ('Media', {
            'fields': ('gallery_images',)
        }),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'event', 'email', 'attendance_status', 'payment_status', 'registration_date']
    list_filter = ['attendance_status', 'payment_status', 'event', 'registration_date']
    search_fields = ['first_name', 'last_name', 'email', 'event__title']
    
    fieldsets = (
        ('Participant Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'organization')
        }),
        ('Registration Status', {
            'fields': ('attendance_status', 'payment_status')
        }),
        ('Additional Information', {
            'fields': ('dietary_requirements', 'special_needs', 'comments')
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'frequency', 'is_subscribed', 'created_at']
    list_filter = ['frequency', 'is_subscribed', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'first_name', 'last_name')
        }),
        ('Preferences', {
            'fields': ('interests', 'frequency')
        }),
        ('Status', {
            'fields': ('is_subscribed', 'confirmed_at', 'unsubscribed_at')
        }),
        ('Tracking', {
            'fields': ('subscription_source',)
        }),
    )
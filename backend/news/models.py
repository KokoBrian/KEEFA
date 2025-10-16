from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field 
from core.models import BaseModel


class NewsCategory(BaseModel):
    """News categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=20, default="primary")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name


class NewsArticle(BaseModel):
    """News articles and updates"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=300)
    content = CKEditor5Field()
    
    # Media
    featured_image = models.ImageField(upload_to='news/')
    gallery_images = models.TextField(blank=True, null=True, help_text="JSON array of image URLs")
    video_url = models.URLField(blank=True, null=True)
    
    # Categorization
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='articles')
    tags = models.CharField(max_length=200, blank=True, null=True, help_text="Comma-separated tags")
    
    # Author and Publishing
    author = models.CharField(max_length=100, default="KEEFA Team")
    publish_date = models.DateTimeField(default=timezone.now)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    
    # Related content
    related_articles = models.ManyToManyField('self', blank=True, symmetrical=False)

    class Meta:
        ordering = ['-publish_date']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def __str__(self):
        return self.title

    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class Event(BaseModel):
    """Upcoming events and activities"""
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('ceremony', 'Ceremony'),
        ('fundraising', 'Fundraising Event'),
        ('community', 'Community Event'),
        ('meeting', 'Meeting'),
        ('conference', 'Conference'),
        ('other', 'Other'),
    ]
    
    EVENT_STATUS = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = CKEditor5Field()
    
    # Event details
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Location
    venue = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    
    # Registration
    requires_registration = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    registration_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Media
    featured_image = models.ImageField(upload_to='events/')
    gallery_images = models.TextField(blank=True, null=True, help_text="JSON array of image URLs")
    
    # Contact
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default='upcoming')
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.end_date < timezone.now()

    @property
    def is_today(self):
        today = timezone.now().date()
        return self.start_date.date() <= today <= self.end_date.date()


class EventRegistration(BaseModel):
    """Event registrations"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    
    # Participant information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    organization = models.CharField(max_length=200, blank=True, null=True)
    
    # Registration details
    registration_date = models.DateTimeField(auto_now_add=True)
    attendance_status = models.CharField(max_length=20, choices=[
        ('registered', 'Registered'),
        ('confirmed', 'Confirmed'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
        ('cancelled', 'Cancelled'),
    ], default='registered')
    
    # Payment (if applicable)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
        ('refunded', 'Refunded'),
    ], default='pending')
    
    # Additional information
    dietary_requirements = models.TextField(blank=True, null=True)
    special_needs = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['event', 'email']
        ordering = ['-registration_date']
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Newsletter(BaseModel):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Preferences
    interests = models.JSONField(blank=True, null=True, help_text="Array of interest categories")
    frequency = models.CharField(max_length=20, choices=[
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ], default='monthly')
    
    # Status
    is_subscribed = models.BooleanField(default=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    
    # Tracking
    subscription_source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.email
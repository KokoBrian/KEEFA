from django.db import models
from django.utils import timezone
from core.models import BaseModel


class ContactInquiry(BaseModel):
    """Contact form submissions"""
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('volunteer', 'Volunteer Opportunities'),
        ('partnership', 'Partnership Proposal'),
        ('donation', 'Donation Information'),
        ('scholarship', 'Scholarship Application'),
        ('media', 'Media Inquiry'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    
    # Inquiry Details
    subject = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    message = models.TextField()
    
    # Newsletter subscription
    subscribe_newsletter = models.BooleanField(default=False)
    
    # Internal tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    
    # Response tracking
    response_sent = models.BooleanField(default=False)
    response_sent_at = models.DateTimeField(blank=True, null=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    
    # Internal notes
    internal_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class OfficeLocation(BaseModel):
    """Office locations and contact information"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Kenya")
    
    # Contact details
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    fax = models.CharField(max_length=20, blank=True, null=True)
    
    # Geographic coordinates
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    
    # Office details
    office_hours = models.TextField(help_text="Office hours description")
    services_offered = models.TextField(blank=True, null=True)
    
    # Status
    is_main_office = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Office Location"
        verbose_name_plural = "Office Locations"

    def __str__(self):
        return f"{self.name}, {self.city}"


class ContactPerson(BaseModel):
    """Key contact persons for different departments"""
    DEPARTMENTS = [
        ('general', 'General Inquiries'),
        ('programs', 'Programs'),
        ('donations', 'Donations & Fundraising'),
        ('partnerships', 'Partnerships'),
        ('media', 'Media Relations'),
        ('volunteer', 'Volunteer Coordination'),
        ('finance', 'Finance'),
        ('admin', 'Administration'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=20, choices=DEPARTMENTS)
    
    # Contact information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    extension = models.CharField(max_length=10, blank=True, null=True)
    
    # Availability
    office_hours = models.CharField(max_length=200, blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, blank=True, null=True)
    
    # Photo and bio
    photo = models.ImageField(upload_to='contact_persons/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Display settings
    is_public = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Contact Person"
        verbose_name_plural = "Contact Persons"

    def __str__(self):
        return f"{self.name} - {self.department}"


class SocialMediaAccount(BaseModel):
    """Social media accounts and links"""
    PLATFORMS = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORMS, unique=True)
    username = models.CharField(max_length=100)
    url = models.URLField()
    follower_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    # Display settings
    is_primary = models.BooleanField(default=False)
    show_in_footer = models.BooleanField(default=True)
    show_in_contact = models.BooleanField(default=True)
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'platform']
        verbose_name = "Social Media Account"
        verbose_name_plural = "Social Media Accounts"

    def __str__(self):
        return f"{self.platform} - @{self.username}"
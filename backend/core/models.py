from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class BaseModel(models.Model):
    """Base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Organization(models.Model):
    """Organization information"""
    name = models.CharField(max_length=200, default="KEEFA")
    tagline = models.CharField(max_length=300, default="Empowering Communities")
    mission = CKEditor5Field()
    vision = CKEditor5Field()
    values = CKEditor5Field()
    story = CKEditor5Field()
    
    # Contact Information
    email = models.EmailField(default="info@keefa.org")
    phone = models.CharField(max_length=20, default="+254 123 456 789")
    address = models.TextField(default="Sheywe Hotel Area, Kakamega, Kenya")
    
    # Social Media
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    
    # Logo and Images
    logo = models.ImageField(upload_to='organization/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='organization/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Organization Information"
        verbose_name_plural = "Organization Information"

    def __str__(self):
        return self.name


class ImpactStatistic(BaseModel):
    """Impact statistics for the homepage"""
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=20)  # e.g., "500+", "95%"
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, help_text="CSS class for icon")
    color = models.CharField(max_length=20, default="primary")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Impact Statistic"
        verbose_name_plural = "Impact Statistics"

    def __str__(self):
        return f"{self.title}: {self.value}"


class TeamMember(BaseModel):
    """Team members and leadership"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.position}"


class Partner(BaseModel):
    """Partner organizations"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='partners/')
    website_url = models.URLField(blank=True, null=True)
    partnership_type = models.CharField(max_length=50, choices=[
        ('corporate', 'Corporate Partner'),
        ('educational', 'Educational Institution'),
        ('government', 'Government Agency'),
        ('ngo', 'NGO/Non-profit'),
        ('foundation', 'Foundation'),
        ('other', 'Other'),
    ])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name


class Testimonial(BaseModel):
    """Success stories and testimonials"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.ImageField(upload_to='testimonials/')
    program_type = models.CharField(max_length=50, choices=[
        ('scholarship', 'Scholarship Program'),
        ('workshop', 'Workshop & Mentorship'),
        ('community', 'Community Project'),
        ('general', 'General'),
    ])
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} - {self.program_type}"


class FAQ(BaseModel):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=300)
    answer = CKEditor5Field()
    category = models.CharField(max_length=50, choices=[
        ('general', 'General'),
        ('scholarships', 'Scholarships'),
        ('donations', 'Donations'),
        ('volunteering', 'Volunteering'),
        ('programs', 'Programs'),
    ])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class SiteSettings(models.Model):
    """Global site settings"""
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True, null=True)
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, default="+254123456789")
    emergency_contact = models.CharField(max_length=20, default="+254111222333")
    
    # SEO Settings
    meta_title = models.CharField(max_length=60, default="KEEFA - Empowering Communities")
    meta_description = models.CharField(max_length=160, default="Empowering futures, building communities through scholarships and community outreach programs")
    meta_keywords = models.CharField(max_length=200, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one SiteSettings instance is allowed")
        super().save(*args, **kwargs)
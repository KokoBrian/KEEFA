from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from core.models import BaseModel


class Program(BaseModel):
    """Main programs offered by the organization"""
    PROGRAM_TYPES = [
        ('scholarship', 'Scholarship Program'),
        ('workshop', 'Workshop & Mentorship'),
        ('community', 'Community Project'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    short_description = models.TextField(max_length=300)
    full_description = CKEditor5Field()
    image = models.ImageField(upload_to='programs/')
    icon = models.CharField(max_length=50, help_text="CSS class for icon")
    color = models.CharField(max_length=20, default="primary")
    
    # Program metrics
    beneficiaries_count = models.PositiveIntegerField(default=0)
    success_rate = models.PositiveIntegerField(default=0, help_text="Percentage")
    
    # Program details
    eligibility_criteria = CKEditor5Field(blank=True, null=True)
    application_process = CKEditor5Field(blank=True, null=True)
    requirements = CKEditor5Field(blank=True, null=True)
    
    # Status
    is_accepting_applications = models.BooleanField(default=True)
    application_deadline = models.DateField(blank=True, null=True)
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Program"
        verbose_name_plural = "Programs"

    def __str__(self):
        return self.name


class ScholarshipApplication(BaseModel):
    """Scholarship applications from students"""
    APPLICATION_STATUS = [
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
    ]
    
    EDUCATION_LEVEL = [
        ('high_school', 'High School'),
        ('college', 'College/University'),
        ('vocational', 'Vocational Training'),
        ('other', 'Other'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    
    # Address
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    
    # Education Information
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL)
    current_school = models.CharField(max_length=200)
    class_year = models.CharField(max_length=50)
    previous_grades = models.TextField(help_text="Previous academic performance")
    
    # Financial Information
    family_income = models.CharField(max_length=100)
    family_size = models.PositiveIntegerField()
    guardian_name = models.CharField(max_length=200)
    guardian_occupation = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    
    # Essay Questions
    why_deserve_scholarship = models.TextField(max_length=1000)
    career_goals = models.TextField(max_length=1000)
    community_involvement = models.TextField(max_length=1000, blank=True, null=True)
    
    # Documents
    academic_transcripts = models.FileField(upload_to='applications/transcripts/', blank=True, null=True)
    recommendation_letter = models.FileField(upload_to='applications/recommendations/', blank=True, null=True)
    financial_documents = models.FileField(upload_to='applications/financial/', blank=True, null=True)
    
    # Application Status
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending')
    review_notes = models.TextField(blank=True, null=True)
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    
    # Scholarship Details (if approved)
    scholarship_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    scholarship_duration = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Scholarship Application"
        verbose_name_plural = "Scholarship Applications"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class WorkshopRegistration(BaseModel):
    """Workshop and mentorship program registrations"""
    WORKSHOP_TYPES = [
        ('life_skills', 'Life Skills Training'),
        ('digital_literacy', 'Digital Literacy'),
        ('career_guidance', 'Career Guidance'),
        ('entrepreneurship', 'Entrepreneurship'),
        ('leadership', 'Leadership Development'),
        ('other', 'Other'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    
    # Location
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    
    # Workshop Preferences
    workshop_type = models.CharField(max_length=20, choices=WORKSHOP_TYPES)
    preferred_schedule = models.CharField(max_length=50, choices=[
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('evenings', 'Evenings'),
        ('flexible', 'Flexible'),
    ])
    
    # Background Information
    education_level = models.CharField(max_length=100)
    current_occupation = models.CharField(max_length=100, blank=True, null=True)
    previous_experience = models.TextField(blank=True, null=True)
    expectations = models.TextField(max_length=500)
    
    # Status
    is_confirmed = models.BooleanField(default=False)
    workshop_batch = models.CharField(max_length=100, blank=True, null=True)
    completion_status = models.CharField(max_length=20, choices=[
        ('registered', 'Registered'),
        ('attending', 'Attending'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped Out'),
    ], default='registered')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Workshop Registration"
        verbose_name_plural = "Workshop Registrations"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.workshop_type}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class ProjectLocation(BaseModel):
    """Community project locations"""
    name = models.CharField(max_length=200)
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    
    # Geographic coordinates
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    
    # Project details
    project_types = models.CharField(max_length=200, help_text="Comma-separated project types")
    description = models.TextField()
    beneficiaries_count = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    
    # Images
    main_image = models.ImageField(upload_to='project_locations/')
    gallery_images = models.TextField(blank=True, null=True, help_text="JSON array of image URLs")
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ], default='active')

    class Meta:
        ordering = ['county', 'name']
        verbose_name = "Project Location"
        verbose_name_plural = "Project Locations"

    def __str__(self):
        return f"{self.name}, {self.county}"


class SuccessStory(BaseModel):
    """Detailed success stories from beneficiaries"""
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='success_stories')
    title = models.CharField(max_length=200)
    story = CKEditor5Field()
    
    # Images and media
    profile_image = models.ImageField(upload_to='success_stories/')
    before_image = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    after_image = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    # Story details
    age = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=100)
    current_status = models.CharField(max_length=200)
    achievements = models.TextField()
    
    # Metrics
    impact_metrics = models.TextField(blank=True, null=True, help_text="JSON format for various metrics")
    
    # Publishing
    is_featured = models.BooleanField(default=False)
    publish_date = models.DateField(default=timezone.now)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-publish_date', 'order']
        verbose_name = "Success Story"
        verbose_name_plural = "Success Stories"

    def __str__(self):
        return f"{self.name} - {self.title}"
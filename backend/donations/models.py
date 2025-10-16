from django.db import models
from django.utils import timezone
from decimal import Decimal
from core.models import BaseModel


class DonationCampaign(BaseModel):
    """Donation campaigns and fundraising initiatives"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Campaign details
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='campaigns/')
    
    # Campaign type
    campaign_type = models.CharField(max_length=50, choices=[
        ('general', 'General Fund'),
        ('scholarship', 'Scholarship Program'),
        ('workshop', 'Workshop & Mentorship'),
        ('community', 'Community Project'),
        ('emergency', 'Emergency Fund'),
        ('infrastructure', 'Infrastructure'),
    ])
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Donation Campaign"
        verbose_name_plural = "Donation Campaigns"

    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        if self.goal_amount > 0:
            return min(100, (self.raised_amount / self.goal_amount) * 100)
        return 0

    @property
    def remaining_amount(self):
        return max(0, self.goal_amount - self.raised_amount)


class Donation(BaseModel):
    """Individual donations"""

    DONATION_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    DONATION_TYPE = [
        ('one_time', 'One-time'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ]

    ALUMNI_DONATION_PERIODS = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]

    # Donor Information
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)
    is_alumni = models.BooleanField(default=False)
    alumni_donation_period = models.CharField(
        max_length=10,
        choices=ALUMNI_DONATION_PERIODS,
        blank=True,
        null=True,
        help_text="For alumni donors: monthly, yearly, or custom"
    )

    # Donation Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE, default='one_time')
    campaign = models.ForeignKey(DonationCampaign, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    # Payment Information
    payment_method = models.CharField(max_length=50, choices=[
        ('stripe', 'Credit/Debit Card'),
        ('mpesa', 'M-Pesa'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('other', 'Other'),
    ])
    transaction_id = models.CharField(max_length=200, unique=True)
    payment_reference = models.CharField(max_length=200, blank=True, null=True)

    # Status and Processing
    status = models.CharField(max_length=20, choices=DONATION_STATUS, default='pending')
    processed_at = models.DateTimeField(blank=True, null=True)

    # Tax and Receipt
    is_tax_deductible = models.BooleanField(default=True)
    receipt_sent = models.BooleanField(default=False)
    receipt_sent_at = models.DateTimeField(blank=True, null=True)

    # Recurring Donations
    is_recurring = models.BooleanField(default=False)
    next_payment_date = models.DateField(blank=True, null=True)
    subscription_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    def __str__(self):
        donor = "Anonymous" if self.is_anonymous else self.donor_name
        return f"{donor} - {self.currency} {self.amount}"

    def get_alumni_default_amount(self):
        """Return alumni default amount based on donation period"""
        if self.alumni_donation_period == 'monthly':
            return 50
        elif self.alumni_donation_period == 'yearly':
            return 600
        elif self.alumni_donation_period == 'custom':
            return self.amount
        return self.amount

    def get_mpesa_account_number(self):
        """Generate M-Pesa paybill account number for alumni"""
        depositor_name = self.donor_name.replace(' ', '').upper() if self.donor_name else "ALUMNI"
        return f"299239#{depositor_name}"

    def save(self, *args, **kwargs):
        # Set alumni default donation_type & amount if alumni
        if self.is_alumni:
            # Set donation_type based on alumni_donation_period
            if self.alumni_donation_period == 'monthly':
                self.donation_type = 'monthly'
                self.amount = 50
                self.is_recurring = True
            elif self.alumni_donation_period == 'yearly':
                self.donation_type = 'annual'
                self.amount = 600
                self.is_recurring = True
            elif self.alumni_donation_period == 'custom':
                self.donation_type = 'one_time'
                self.is_recurring = False
                # amount is expected to be set manually for custom donations

            # Ensure currency is KES for alumni donations
            self.currency = 'KES'

            # Default payment method for alumni
            if not self.payment_method:
                self.payment_method = 'mpesa'

        # Update campaign raised amount when donation is completed
        if self.status == 'completed' and self.campaign:
            if self.pk:  # Existing donation
                old_donation = Donation.objects.get(pk=self.pk)
                if old_donation.status != 'completed':
                    self.campaign.raised_amount += self.amount
                    self.campaign.save()
            else:  # New donation
                self.campaign.raised_amount += self.amount
                self.campaign.save()

        super().save(*args, **kwargs)

class DonationImpact(BaseModel):
    """Track how donations are used and their impact"""
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='impact')
    
    # Impact details
    impact_description = models.TextField()
    beneficiaries_count = models.PositiveIntegerField(default=0)
    impact_metrics = models.JSONField(blank=True, null=True)
    
    # Media
    impact_images = models.TextField(blank=True, null=True, help_text="JSON array of image URLs")
    impact_video_url = models.URLField(blank=True, null=True)
    
    # Reporting
    report_date = models.DateField()
    report_sent = models.BooleanField(default=False)
    report_sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Donation Impact"
        verbose_name_plural = "Donation Impacts"

    def __str__(self):
        return f"Impact for {self.donation}"


class Volunteer(BaseModel):
    """Volunteer registrations"""
    VOLUNTEER_INTERESTS = [
        ('mentorship', 'Student Mentorship'),
        ('workshops', 'Workshop Facilitation'),
        ('community', 'Community Projects'),
        ('admin', 'Administrative Support'),
        ('media', 'Documentation & Media'),
        ('fundraising', 'Fundraising & Outreach'),
        ('other', 'Other'),
    ]
    
    AVAILABILITY = [
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('evenings', 'Evenings'),
        ('flexible', 'Flexible'),
        ('events', 'Events only'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    
    # Volunteer Details
    interests = models.JSONField(help_text="Array of interest areas")
    skills_experience = models.TextField()
    availability = models.CharField(max_length=20, choices=AVAILABILITY)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('rejected', 'Rejected'),
    ], default='pending')
    
    # Volunteer tracking
    hours_contributed = models.PositiveIntegerField(default=0)
    projects_participated = models.PositiveIntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    
    # Notes
    admin_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Partnership(BaseModel):
    """Partnership inquiries and collaborations"""
    ORGANIZATION_TYPES = [
        ('corporate', 'Corporate/Business'),
        ('educational', 'Educational Institution'),
        ('government', 'Government Agency'),
        ('ngo', 'NGO/Non-profit'),
        ('foundation', 'Foundation'),
        ('other', 'Other'),
    ]
    
    PARTNERSHIP_TYPES = [
        ('funding', 'Funding Support'),
        ('volunteer', 'Employee Volunteering'),
        ('skills', 'Skills-based Support'),
        ('resources', 'Resource Sharing'),
        ('joint', 'Joint Programs'),
        ('advocacy', 'Advocacy'),
    ]
    
    # Organization Information
    organization_name = models.CharField(max_length=200)
    organization_type = models.CharField(max_length=20, choices=ORGANIZATION_TYPES)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Partnership Details
    partnership_interests = models.JSONField(help_text="Array of partnership types")
    proposal_details = models.TextField()
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('active', 'Active Partnership'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ], default='pending')
    
    # Follow-up
    follow_up_date = models.DateField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Partnership"
        verbose_name_plural = "Partnerships"

    def __str__(self):
        return f"{self.organization_name} - {self.contact_person}"
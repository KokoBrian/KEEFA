from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # User type
    USER_TYPES = [
        ('admin', 'Administrator'),
        ('staff', 'Staff Member'),
        ('volunteer', 'Volunteer'),
        ('donor', 'Donor'),
        ('beneficiary', 'Beneficiary'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='donor')
    
    # Preferences
    newsletter_subscribed = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    
    # Tracking
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add unique related_name arguments to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser_permissions',
    )

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
from rest_framework import serializers
from .models import ContactInquiry, OfficeLocation, ContactPerson, SocialMediaAccount


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'organization',
            'subject', 'message', 'subscribe_newsletter'
        ]


class OfficeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeLocation
        fields = [
            'id', 'name', 'address', 'city', 'county', 'postal_code', 'country',
            'phone', 'email', 'latitude', 'longitude', 'office_hours',
            'services_offered', 'is_main_office'
        ]


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = [
            'id', 'name', 'position', 'department', 'email', 'phone',
            'extension', 'office_hours', 'languages_spoken', 'photo', 'bio'
        ]


class SocialMediaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaAccount
        fields = [
            'id', 'platform', 'username', 'url', 'follower_count', 'is_primary'
        ]
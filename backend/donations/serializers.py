from rest_framework import serializers
from .models import DonationCampaign, Donation, Volunteer, Partnership


class DonationCampaignSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = DonationCampaign
        fields = [
            'id', 'title', 'slug', 'description', 'goal_amount', 'raised_amount',
            'progress_percentage', 'remaining_amount', 'start_date', 'end_date',
            'image', 'campaign_type', 'is_featured', 'is_urgent'
        ]


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [
            'donor_name', 'donor_email', 'donor_phone', 'is_anonymous',
            'amount', 'currency', 'donation_type', 'campaign', 'designation',
            'message', 'payment_method'
        ]


class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'location',
            'interests', 'skills_experience', 'availability'
        ]


class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = [
            'organization_name', 'organization_type', 'contact_person',
            'email', 'phone', 'website', 'partnership_interests',
            'proposal_details'
        ]
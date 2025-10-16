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
            'donor_name',
            'donor_email',
            'donor_phone',
            'is_anonymous',
            'is_alumni',
            'alumni_donation_period',
            'amount',
            'currency',
            'donation_type',
            'campaign',
            'designation',
            'message',
            'payment_method',
        ]
        extra_kwargs = {
            'currency': {'default': 'KES'},
            'donation_type': {'default': 'one_time'},
            'payment_method': {'default': 'mpesa'},
        }

    def validate(self, data):
        is_alumni = data.get('is_alumni', False)
        alumni_period = data.get('alumni_donation_period', None)
        amount = data.get('amount', None)

        if is_alumni:
            if alumni_period not in ['monthly', 'yearly', 'custom']:
                raise serializers.ValidationError({
                    'alumni_donation_period': "Must be 'monthly', 'yearly', or 'custom' for alumni donations."
                })

            # Override amount for monthly/yearly alumni defaults
            if alumni_period == 'monthly':
                data['amount'] = 50
                data['donation_type'] = 'monthly'
                data['payment_method'] = 'mpesa'
            elif alumni_period == 'yearly':
                data['amount'] = 600
                data['donation_type'] = 'annual'
                data['payment_method'] = 'mpesa'
            elif alumni_period == 'custom':
                # For custom, amount must be provided and > 0
                if amount is None or amount <= 0:
                    raise serializers.ValidationError({
                        'amount': "Custom alumni donations must specify a positive amount."
                    })
                data['donation_type'] = 'one_time'
                data['payment_method'] = 'mpesa'

            # Force currency to KES for alumni
            data['currency'] = 'KES'

        return data


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
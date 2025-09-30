from rest_framework import serializers
from .models import (
    Organization, ImpactStatistic, TeamMember, Partner, 
    Testimonial, FAQ, SiteSettings
)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ImpactStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactStatistic
        fields = ['id', 'title', 'value', 'description', 'icon', 'color', 'order']


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'position', 'bio', 'photo', 'email', 'linkedin_url', 'order']


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'description', 'logo', 'website_url', 'partnership_type', 'order']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'position', 'content', 'photo', 'program_type', 'rating', 'is_featured']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category']


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'maintenance_mode', 'maintenance_message', 'whatsapp_number', 
            'emergency_contact', 'meta_title', 'meta_description', 'meta_keywords'
        ]
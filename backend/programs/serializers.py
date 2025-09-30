from rest_framework import serializers
from .models import (
    Program, ScholarshipApplication, WorkshopRegistration, 
    ProjectLocation, SuccessStory
)


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'id', 'name', 'slug', 'program_type', 'short_description', 
            'full_description', 'image', 'icon', 'color', 'beneficiaries_count', 
            'success_rate', 'is_accepting_applications', 'application_deadline'
        ]


class ProgramDetailSerializer(serializers.ModelSerializer):
    success_stories = serializers.SerializerMethodField()
    
    class Meta:
        model = Program
        fields = [
            'id', 'name', 'slug', 'program_type', 'short_description', 
            'full_description', 'image', 'icon', 'color', 'beneficiaries_count', 
            'success_rate', 'eligibility_criteria', 'application_process', 
            'requirements', 'is_accepting_applications', 'application_deadline',
            'success_stories'
        ]
    
    def get_success_stories(self, obj):
        stories = obj.success_stories.filter(is_active=True)[:3]
        return SuccessStorySerializer(stories, many=True).data


class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipApplication
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender',
            'county', 'sub_county', 'ward', 'village', 'education_level', 
            'current_school', 'class_year', 'previous_grades', 'family_income',
            'family_size', 'guardian_name', 'guardian_occupation', 'guardian_phone',
            'why_deserve_scholarship', 'career_goals', 'community_involvement',
            'academic_transcripts', 'recommendation_letter', 'financial_documents'
        ]


class WorkshopRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopRegistration
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'age', 'gender',
            'county', 'sub_county', 'workshop_type', 'preferred_schedule',
            'education_level', 'current_occupation', 'previous_experience',
            'expectations'
        ]


class ProjectLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLocation
        fields = [
            'id', 'name', 'county', 'sub_county', 'ward', 'latitude', 'longitude',
            'project_types', 'description', 'beneficiaries_count', 'start_date',
            'main_image', 'gallery_images', 'status'
        ]


class SuccessStorySerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    
    class Meta:
        model = SuccessStory
        fields = [
            'id', 'name', 'program_name', 'title', 'story', 'profile_image',
            'before_image', 'after_image', 'video_url', 'age', 'location',
            'current_status', 'achievements', 'impact_metrics', 'publish_date'
        ]


class SuccessStoryListSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    
    class Meta:
        model = SuccessStory
        fields = [
            'id', 'name', 'program_name', 'title', 'profile_image',
            'location', 'current_status', 'publish_date'
        ]
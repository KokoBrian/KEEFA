from rest_framework import serializers
from .models import NewsCategory, NewsArticle, Event, EventRegistration, Newsletter


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name', 'slug', 'description', 'color']


class NewsArticleListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image', 'category_name',
            'category_color', 'author', 'publish_date', 'views_count', 'tags_list'
        ]
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()


class NewsArticleDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    tags_list = serializers.SerializerMethodField()
    related_articles = NewsArticleListSerializer(many=True, read_only=True)
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'gallery_images', 'video_url', 'category_name', 'category_color',
            'author', 'publish_date', 'views_count', 'tags_list', 'related_articles',
            'meta_title', 'meta_description'
        ]
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()


class EventListSerializer(serializers.ModelSerializer):
    is_past = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'event_type', 'start_date', 'end_date',
            'venue', 'featured_image', 'requires_registration', 'registration_fee',
            'status', 'is_featured', 'is_past', 'is_today'
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    is_past = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()
    registrations_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'event_type', 'start_date',
            'end_date', 'venue', 'address', 'latitude', 'longitude',
            'requires_registration', 'registration_deadline', 'max_participants',
            'registration_fee', 'featured_image', 'gallery_images',
            'contact_person', 'contact_email', 'contact_phone', 'status',
            'is_featured', 'is_past', 'is_today', 'registrations_count'
        ]
    
    def get_registrations_count(self, obj):
        return obj.registrations.filter(attendance_status__in=['registered', 'confirmed']).count()


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'organization',
            'dietary_requirements', 'special_needs', 'comments'
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email', 'first_name', 'last_name', 'interests', 'frequency']
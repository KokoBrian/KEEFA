from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import NewsCategory, NewsArticle, Event, EventRegistration, Newsletter
from .serializers import (
    NewsCategorySerializer, NewsArticleListSerializer, NewsArticleDetailSerializer,
    EventListSerializer, EventDetailSerializer, EventRegistrationSerializer,
    NewsletterSerializer
)


class NewsCategoriesListView(generics.ListAPIView):
    """List all active news categories"""
    serializer_class = NewsCategorySerializer
    queryset = NewsCategory.objects.filter(is_active=True)


class NewsArticlesListView(generics.ListAPIView):
    """List all published news articles"""
    serializer_class = NewsArticleListSerializer
    queryset = NewsArticle.objects.filter(is_published=True, is_active=True)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset


class FeaturedNewsListView(generics.ListAPIView):
    """List featured news articles"""
    serializer_class = NewsArticleListSerializer
    queryset = NewsArticle.objects.filter(
        is_published=True, is_active=True, is_featured=True
    )[:5]


class NewsArticleDetailView(generics.RetrieveAPIView):
    """Get news article details by slug"""
    serializer_class = NewsArticleDetailSerializer
    lookup_field = 'slug'
    queryset = NewsArticle.objects.filter(is_published=True, is_active=True)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class EventsListView(generics.ListAPIView):
    """List all active events"""
    serializer_class = EventListSerializer
    queryset = Event.objects.filter(is_active=True)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        event_type = self.request.query_params.get('type', None)
        status_filter = self.request.query_params.get('status', None)
        
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        if status_filter == 'upcoming':
            queryset = queryset.filter(start_date__gte=timezone.now())
        elif status_filter == 'past':
            queryset = queryset.filter(end_date__lt=timezone.now())
        
        return queryset


class UpcomingEventsListView(generics.ListAPIView):
    """List upcoming events"""
    serializer_class = EventListSerializer
    queryset = Event.objects.filter(
        is_active=True, 
        start_date__gte=timezone.now()
    ).order_by('start_date')[:5]


class EventDetailView(generics.RetrieveAPIView):
    """Get event details by slug"""
    serializer_class = EventDetailSerializer
    lookup_field = 'slug'
    queryset = Event.objects.filter(is_active=True)

class EventRegistrationCreateView(generics.CreateAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication] 

    def create(self, request, *args, **kwargs):
        event_slug = request.data.get("event_slug")
    
        if not event_slug:
            return Response({"error": "event_slug is required"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            event = Event.objects.get(slug=event_slug, is_active=True)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Validate serializer data except event_slug
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicate registration
        email = serializer.validated_data.get('email')
        if EventRegistration.objects.filter(event=event, email=email).exists():
            return Response({"message": "Already registered for this event"}, status=status.HTTP_200_OK)

        # Save registration with linked event
        registration = serializer.save(event=event)
        return Response(
            {"message": f"Successfully registered for {event.title}!", "id": registration.id},
            status=status.HTTP_201_CREATED
        )       
  

class NewsletterSubscribeView(generics.CreateAPIView):
    """Subscribe to newsletter"""
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if Newsletter.objects.filter(email=email).exists():
            return Response(
                {'message': 'Email already subscribed'}, 
                status=status.HTTP_200_OK
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            subscription = serializer.save()
            return Response(
                {
                    'message': 'Successfully subscribed to newsletter',
                    'subscription_id': subscription.id
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def news_overview(request):
    """Get overview data for news page"""
    try:
        featured_article = NewsArticle.objects.filter(
            is_published=True, is_active=True, is_featured=True
        ).first()
        
        recent_articles = NewsArticle.objects.filter(
            is_published=True, is_active=True
        ).exclude(id=featured_article.id if featured_article else None)[:6]
        
        upcoming_events = Event.objects.filter(
            is_active=True, 
            start_date__gte=timezone.now()
        ).order_by('start_date')[:3]
        
        data = {
            'featured_article': NewsArticleDetailSerializer(featured_article).data if featured_article else None,
            'recent_articles': NewsArticleListSerializer(recent_articles, many=True).data,
            'upcoming_events': EventListSerializer(upcoming_events, many=True).data,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch news overview'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
from django.urls import path
from .views import (
    NewsCategoriesListView, NewsArticlesListView, FeaturedNewsListView,
    NewsArticleDetailView, EventsListView, UpcomingEventsListView,
    EventDetailView, EventRegistrationCreateView, NewsletterSubscribeView,
    news_overview
)

urlpatterns = [
    path('categories/', NewsCategoriesListView.as_view(), name='news-categories'),
    path('articles/', NewsArticlesListView.as_view(), name='news-articles'),
    path('articles/featured/', FeaturedNewsListView.as_view(), name='featured-news'),
    path('articles/<slug:slug>/', NewsArticleDetailView.as_view(), name='news-article-detail'),
    path('events/', EventsListView.as_view(), name='events-list'),
    path('events/upcoming/', UpcomingEventsListView.as_view(), name='upcoming-events'),
    path('events/<slug:slug>/', EventDetailView.as_view(), name='event-detail'),
    path('events/register/', EventRegistrationCreateView.as_view(), name='event-registration'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('overview/', news_overview, name='news-overview'),
]
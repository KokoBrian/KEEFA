from django.urls import path
from .views import (
    OrganizationDetailView, ImpactStatisticsListView, TeamMembersListView,
    PartnersListView, TestimonialsListView, FeaturedTestimonialsListView,
    FAQListView, SiteSettingsDetailView, homepage_data, about_data
)

urlpatterns = [
    path('organization/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('impact-statistics/', ImpactStatisticsListView.as_view(), name='impact-statistics'),
    path('team-members/', TeamMembersListView.as_view(), name='team-members'),
    path('partners/', PartnersListView.as_view(), name='partners'),
    path('testimonials/', TestimonialsListView.as_view(), name='testimonials'),
    path('testimonials/featured/', FeaturedTestimonialsListView.as_view(), name='featured-testimonials'),
    path('faqs/', FAQListView.as_view(), name='faqs'),
    path('site-settings/', SiteSettingsDetailView.as_view(), name='site-settings'),
    path('homepage-data/', homepage_data, name='homepage-data'),
    path('about-data/', about_data, name='about-data'),
]
from django.urls import path
from .views import (
    ProgramsListView, ProgramDetailView, ScholarshipApplicationCreateView,
    WorkshopRegistrationCreateView, ProjectLocationsListView, 
    SuccessStoriesListView, SuccessStoryDetailView, FeaturedSuccessStoriesListView,
    programs_overview, impact_data
)

urlpatterns = [
    path('', ProgramsListView.as_view(), name='programs-list'),
    path('<slug:slug>/', ProgramDetailView.as_view(), name='program-detail'),
    path('applications/scholarship/', ScholarshipApplicationCreateView.as_view(), name='scholarship-application'),
    path('registrations/workshop/', WorkshopRegistrationCreateView.as_view(), name='workshop-registration'),
    path('locations/', ProjectLocationsListView.as_view(), name='project-locations'),
    path('success-stories/', SuccessStoriesListView.as_view(), name='success-stories'),
    path('success-stories/featured/', FeaturedSuccessStoriesListView.as_view(), name='featured-success-stories'),
    path('success-stories/<int:pk>/', SuccessStoryDetailView.as_view(), name='success-story-detail'),
    path('overview/', programs_overview, name='programs-overview'),
    path('impact-data/', impact_data, name='impact-data'),
]
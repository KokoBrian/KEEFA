from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Program, ScholarshipApplication, WorkshopRegistration, 
    ProjectLocation, SuccessStory
)
from .serializers import (
    ProgramSerializer, ProgramDetailSerializer, ScholarshipApplicationSerializer,
    WorkshopRegistrationSerializer, ProjectLocationSerializer, 
    SuccessStorySerializer, SuccessStoryListSerializer
)


class ProgramsListView(generics.ListAPIView):
    """List all active programs"""
    serializer_class = ProgramSerializer
    queryset = Program.objects.filter(is_active=True)


class ProgramDetailView(generics.RetrieveAPIView):
    """Get program details by slug"""
    serializer_class = ProgramDetailSerializer
    lookup_field = 'slug'
    queryset = Program.objects.filter(is_active=True)


class ScholarshipApplicationCreateView(generics.CreateAPIView):
    """Submit scholarship application"""
    serializer_class = ScholarshipApplicationSerializer
    queryset = ScholarshipApplication.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            return Response(
                {
                    'message': 'Application submitted successfully',
                    'application_id': application.id
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkshopRegistrationCreateView(generics.CreateAPIView):
    """Register for workshop"""
    serializer_class = WorkshopRegistrationSerializer
    queryset = WorkshopRegistration.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            registration = serializer.save()
            return Response(
                {
                    'message': 'Registration submitted successfully',
                    'registration_id': registration.id
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectLocationsListView(generics.ListAPIView):
    """List all active project locations"""
    serializer_class = ProjectLocationSerializer
    queryset = ProjectLocation.objects.filter(is_active=True)


class SuccessStoriesListView(generics.ListAPIView):
    """List all active success stories"""
    serializer_class = SuccessStoryListSerializer
    queryset = SuccessStory.objects.filter(is_active=True)


class SuccessStoryDetailView(generics.RetrieveAPIView):
    """Get success story details"""
    serializer_class = SuccessStorySerializer
    queryset = SuccessStory.objects.filter(is_active=True)


class FeaturedSuccessStoriesListView(generics.ListAPIView):
    """List featured success stories"""
    serializer_class = SuccessStorySerializer
    queryset = SuccessStory.objects.filter(is_active=True, is_featured=True)


@api_view(['GET'])
def programs_overview(request):
    """Get overview data for programs page"""
    try:
        programs = Program.objects.filter(is_active=True)
        featured_stories = SuccessStory.objects.filter(is_active=True, is_featured=True)[:6]
        
        data = {
            'programs': ProgramSerializer(programs, many=True).data,
            'featured_stories': SuccessStoryListSerializer(featured_stories, many=True).data,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch programs overview'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def impact_data(request):
    """Get impact data for impact page"""
    try:
        success_stories = SuccessStory.objects.filter(is_active=True)
        project_locations = ProjectLocation.objects.filter(is_active=True)
        
        # Calculate impact metrics
        total_beneficiaries = sum(location.beneficiaries_count for location in project_locations)
        total_projects = project_locations.count()
        total_stories = success_stories.count()
        
        data = {
            'success_stories': SuccessStorySerializer(success_stories, many=True).data,
            'impact_metrics': {
                'total_beneficiaries': total_beneficiaries,
                'total_projects': total_projects,
                'total_stories': total_stories,
                'active_locations': project_locations.filter(status='active').count(),
            }
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch impact data'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Organization, ImpactStatistic, TeamMember, Partner, 
    Testimonial, FAQ, SiteSettings
)
from .serializers import (
    OrganizationSerializer, ImpactStatisticSerializer, TeamMemberSerializer,
    PartnerSerializer, TestimonialSerializer, FAQSerializer, SiteSettingsSerializer
)


class OrganizationDetailView(generics.RetrieveAPIView):
    """Get organization information"""
    serializer_class = OrganizationSerializer
    
    def get_object(self):
        return Organization.objects.first()


class ImpactStatisticsListView(generics.ListAPIView):
    """List all active impact statistics"""
    serializer_class = ImpactStatisticSerializer
    queryset = ImpactStatistic.objects.filter(is_active=True)


class TeamMembersListView(generics.ListAPIView):
    """List all active team members"""
    serializer_class = TeamMemberSerializer
    queryset = TeamMember.objects.filter(is_active=True)


class PartnersListView(generics.ListAPIView):
    """List all active partners"""
    serializer_class = PartnerSerializer
    queryset = Partner.objects.filter(is_active=True)


class TestimonialsListView(generics.ListAPIView):
    """List all active testimonials"""
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.filter(is_active=True)


class FeaturedTestimonialsListView(generics.ListAPIView):
    """List featured testimonials"""
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.filter(is_active=True, is_featured=True)


class FAQListView(generics.ListAPIView):
    """List all active FAQs"""
    serializer_class = FAQSerializer
    queryset = FAQ.objects.filter(is_active=True)


class SiteSettingsDetailView(generics.RetrieveAPIView):
    """Get site settings"""
    serializer_class = SiteSettingsSerializer
    
    def get_object(self):
        return SiteSettings.objects.first()


@api_view(['GET'])
def homepage_data(request):
    """Get all data needed for homepage"""
    try:
        organization = Organization.objects.first()
        impact_stats = ImpactStatistic.objects.filter(is_active=True)
        featured_testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:3]
        
        data = {
            'organization': OrganizationSerializer(organization).data if organization else None,
            'impact_statistics': ImpactStatisticSerializer(impact_stats, many=True).data,
            'featured_testimonials': TestimonialSerializer(featured_testimonials, many=True).data,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch homepage data'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def about_data(request):
    """Get all data needed for about page"""
    try:
        organization = Organization.objects.first()
        team_members = TeamMember.objects.filter(is_active=True)
        partners = Partner.objects.filter(is_active=True)
        
        data = {
            'organization': OrganizationSerializer(organization).data if organization else None,
            'team_members': TeamMemberSerializer(team_members, many=True).data,
            'partners': PartnerSerializer(partners, many=True).data,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch about data'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
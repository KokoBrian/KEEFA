from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import ContactInquiry, OfficeLocation, ContactPerson, SocialMediaAccount
from .serializers import (
    ContactInquirySerializer, OfficeLocationSerializer, 
    ContactPersonSerializer, SocialMediaAccountSerializer
)

class ContactInquiryCreateView(generics.CreateAPIView):
    """Submit contact inquiry"""
    serializer_class = ContactInquirySerializer
    queryset = ContactInquiry.objects.all()
    permission_classes = [AllowAny] 
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
         inquiry = serializer.save()
        
        # Subscribe to newsletter if requested
        if inquiry.subscribe_newsletter:
            from news.models import Newsletter
            Newsletter.objects.get_or_create(
                email=inquiry.email,
                defaults={
                    'first_name': inquiry.first_name,
                    'last_name': inquiry.last_name,
                    'subscription_source': 'contact_form'
                }
            )
        
        # Successful response with `success` field
        return Response(
            {
                'success': True,
                'message': 'Your message has been sent successfully. We will get back to you soon.',
                'inquiry_id': inquiry.id
            },
            status=status.HTTP_201_CREATED
        )
    
        # If serializer is invalid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OfficeLocationsListView(generics.ListAPIView):
    """List all public office locations"""
    serializer_class = OfficeLocationSerializer
    queryset = OfficeLocation.objects.filter(is_public=True, is_active=True)


class ContactPersonsListView(generics.ListAPIView):
    """List all public contact persons"""
    serializer_class = ContactPersonSerializer
    queryset = ContactPerson.objects.filter(is_public=True, is_active=True)


class SocialMediaAccountsListView(generics.ListAPIView):
    """List all social media accounts"""
    serializer_class = SocialMediaAccountSerializer
    queryset = SocialMediaAccount.objects.filter(is_active=True)


@api_view(['GET'])
def contact_page_data(request):
    """Get all data needed for contact page"""
    try:
        office_locations = OfficeLocation.objects.filter(is_public=True, is_active=True)
        contact_persons = ContactPerson.objects.filter(is_public=True, is_active=True)
        social_media = SocialMediaAccount.objects.filter(show_in_contact=True, is_active=True)
        
        data = {
            'office_locations': OfficeLocationSerializer(office_locations, many=True).data,
            'contact_persons': ContactPersonSerializer(contact_persons, many=True).data,
            'social_media': SocialMediaAccountSerializer(social_media, many=True).data,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch contact page data'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def footer_social_media(request):
    """Get social media accounts for footer"""
    try:
        social_media = SocialMediaAccount.objects.filter(show_in_footer=True, is_active=True)
        data = SocialMediaAccountSerializer(social_media, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch social media data'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
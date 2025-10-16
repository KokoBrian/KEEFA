from django.urls import path
from .views import (
    ContactInquiryCreateView, OfficeLocationsListView, ContactPersonsListView,
    SocialMediaAccountsListView, contact_page_data, footer_social_media
)

urlpatterns = [
    path('inquiries/', ContactInquiryCreateView.as_view(), name='contact-inquiry'),
    path('offices/', OfficeLocationsListView.as_view(), name='office-locations'),
    path('persons/', ContactPersonsListView.as_view(), name='contact-persons'),
    path('social-media/', SocialMediaAccountsListView.as_view(), name='social-media'),
    path('page-data/', contact_page_data, name='contact-page-data'),
    path('footer-social/', footer_social_media, name='footer-social-media'),
]
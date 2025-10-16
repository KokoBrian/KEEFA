from django.urls import path
from .views import (
    DonationCampaignsListView, FeaturedCampaignsListView, DonationCampaignDetailView,
    create_donation, stripe_webhook, mpesa_stk, VolunteerCreateView, PartnershipCreateView,
    donation_stats
)

urlpatterns = [
    path('campaigns/', DonationCampaignsListView.as_view(), name='donation-campaigns'),
    path('campaigns/featured/', FeaturedCampaignsListView.as_view(), name='featured-campaigns'),
    path('campaigns/<slug:slug>/', DonationCampaignDetailView.as_view(), name='campaign-detail'),
    path('create/', create_donation, name='create-donation'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('mpesa-callback/', mpesa_stk, name='mpesa_stk'),
    path('volunteers/', VolunteerCreateView.as_view(), name='volunteer-create'),
    path('partnerships/', PartnershipCreateView.as_view(), name='partnership-create'),
    path('stats/', donation_stats, name='donation-stats'),
]
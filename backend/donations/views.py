from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import stripe
import uuid
from .models import DonationCampaign, Donation, Volunteer, Partnership
from .serializers import (
    DonationCampaignSerializer, DonationSerializer, 
    VolunteerSerializer, PartnershipSerializer
)

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


class DonationCampaignsListView(generics.ListAPIView):
    """List all active donation campaigns"""
    serializer_class = DonationCampaignSerializer
    queryset = DonationCampaign.objects.filter(is_active=True)


class FeaturedCampaignsListView(generics.ListAPIView):
    """List featured donation campaigns"""
    serializer_class = DonationCampaignSerializer
    queryset = DonationCampaign.objects.filter(is_active=True, is_featured=True)


class DonationCampaignDetailView(generics.RetrieveAPIView):
    """Get campaign details by slug"""
    serializer_class = DonationCampaignSerializer
    lookup_field = 'slug'
    queryset = DonationCampaign.objects.filter(is_active=True)


@api_view(['POST'])
def create_donation(request):
    """Create a new donation"""
    try:
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            
            # Create donation record
            donation = serializer.save(
                transaction_id=transaction_id,
                status='pending'
            )
            
            # Process payment based on method
            payment_method = request.data.get('payment_method', 'stripe')
            
            if payment_method == 'stripe':
                try:
                    # Create Stripe payment intent
                    intent = stripe.PaymentIntent.create(
                        amount=int(donation.amount * 100),  # Convert to cents
                        currency=donation.currency.lower(),
                        metadata={
                            'donation_id': donation.id,
                            'donor_name': donation.donor_name,
                            'donor_email': donation.donor_email,
                        }
                    )
                    
                    donation.payment_reference = intent.id
                    donation.save()
                    
                    return Response({
                        'message': 'Donation created successfully',
                        'donation_id': donation.id,
                        'client_secret': intent.client_secret,
                        'payment_intent_id': intent.id
                    }, status=status.HTTP_201_CREATED)
                    
                except stripe.error.StripeError as e:
                    donation.status = 'failed'
                    donation.save()
                    return Response(
                        {'error': f'Payment processing failed: {str(e)}'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            else:
                # For other payment methods, return success with instructions
                return Response({
                    'message': 'Donation created successfully',
                    'donation_id': donation.id,
                    'payment_instructions': f'Please complete payment via {payment_method}'
                }, status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(
            {'error': 'Failed to create donation'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return Response({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return Response({'error': 'Invalid signature'}, status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        try:
            donation = Donation.objects.get(payment_reference=payment_intent['id'])
            donation.status = 'completed'
            donation.save()
        except Donation.DoesNotExist:
            pass
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        try:
            donation = Donation.objects.get(payment_reference=payment_intent['id'])
            donation.status = 'failed'
            donation.save()
        except Donation.DoesNotExist:
            pass
    
    return Response({'status': 'success'})


class VolunteerCreateView(generics.CreateAPIView):
    """Submit volunteer application"""
    serializer_class = VolunteerSerializer
    queryset = Volunteer.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            volunteer = serializer.save()
            return Response(
                {
                    'message': 'Volunteer application submitted successfully',
                    'volunteer_id': volunteer.id
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnershipCreateView(generics.CreateAPIView):
    """Submit partnership inquiry"""
    serializer_class = PartnershipSerializer
    queryset = Partnership.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            partnership = serializer.save()
            return Response(
                {
                    'message': 'Partnership inquiry submitted successfully',
                    'partnership_id': partnership.id
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def donation_stats(request):
    """Get donation statistics"""
    try:
        total_donations = Donation.objects.filter(status='completed').count()
        total_amount = sum(
            donation.amount for donation in 
            Donation.objects.filter(status='completed')
        )
        active_campaigns = DonationCampaign.objects.filter(is_active=True).count()
        active_volunteers = Volunteer.objects.filter(status='active').count()
        
        data = {
            'total_donations': total_donations,
            'total_amount': total_amount,
            'active_campaigns': active_campaigns,
            'active_volunteers': active_volunteers,
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch donation stats'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
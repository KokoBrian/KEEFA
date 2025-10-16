from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import uuid
from .utils import initiate_mpesa_stk_push

 

from .models import DonationCampaign, Donation, Volunteer, Partnership
from .serializers import (
    DonationCampaignSerializer, DonationSerializer,
    VolunteerSerializer, PartnershipSerializer
)

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


# 🔐 Public API View Mixin
class PublicAPIView:
    permission_classes = [AllowAny]


# 📢 Donation Campaign Views

class DonationCampaignsListView(PublicAPIView, generics.ListAPIView):
    """List all active donation campaigns"""
    serializer_class = DonationCampaignSerializer
    queryset = DonationCampaign.objects.filter(is_active=True)


class FeaturedCampaignsListView(PublicAPIView, generics.ListAPIView):
    """List featured donation campaigns"""
    serializer_class = DonationCampaignSerializer
    queryset = DonationCampaign.objects.filter(is_active=True, is_featured=True)


class DonationCampaignDetailView(PublicAPIView, generics.RetrieveAPIView):
    """Get campaign details by slug"""
    serializer_class = DonationCampaignSerializer
    lookup_field = 'slug'
    queryset = DonationCampaign.objects.filter(is_active=True)


# 💰 Donation Handling

@api_view(['POST'])
@permission_classes([AllowAny])
def create_donation(request):
    """Create a new donation, defaults to M-Pesa payment."""
    serializer = DonationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    payment_method = request.data.get('payment_method', 'mpesa').lower()
    transaction_id = str(uuid.uuid4())

    donation = serializer.save(transaction_id=transaction_id, status='pending')

    try:
        if payment_method == 'mpesa':
            # Expect phone number in donation.phone_number (make sure your serializer/model supports this)
            response = initiate_mpesa_stk_push(donation)
            donation.payment_reference = response.get('CheckoutRequestID', '')
            donation.save()

            return Response({
                'message': 'M-Pesa payment initiated. Please complete payment on your phone.',
                'donation_id': donation.id,
                'checkout_request_id': donation.payment_reference,
            }, status=status.HTTP_201_CREATED)

        elif payment_method == 'stripe':
            import stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY

            intent = stripe.PaymentIntent.create(
                amount=int(donation.amount * 100),  # cents
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
                'message': 'Stripe payment initiated.',
                'donation_id': donation.id,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
            }, status=status.HTTP_201_CREATED)

        else:
            # Other payment methods can be handled here
            return Response({
                'message': 'Donation created successfully.',
                'donation_id': donation.id,
                'payment_instructions': f'Please complete payment via {payment_method}.'
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        donation.status = 'failed'
        donation.save()
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])

def mpesa_stk(request):
    """Handle M-Pesa STK push callback."""
    try:
        data = request.data
        body = data.get('Body', {})
        stk_callback = body.get('stkCallback', {})
        result_code = stk_callback.get('ResultCode')
        checkout_request_id = stk_callback.get('CheckoutRequestID')

        donation = Donation.objects.filter(payment_reference=checkout_request_id).first()
        if not donation:
            return Response({'error': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)

        if result_code == 0:
            donation.status = 'completed'
        else:
            donation.status = 'failed'

        donation.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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


# 👥 Public Submission Forms

class VolunteerCreateView(PublicAPIView, generics.CreateAPIView):
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


class PartnershipCreateView(PublicAPIView, generics.CreateAPIView):
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


# 📊 Donation Statistics

@api_view(['GET'])
@permission_classes([AllowAny])
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
    except Exception:
        return Response(
            {'error': 'Failed to fetch donation stats'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

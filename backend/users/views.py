from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserProfileSerializer, LoginSerializer


class UserRegistrationView(generics.CreateAPIView):
    """User registration"""
    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'message': 'User registered successfully',
                    'user_id': user.id,
                    'token': token.key
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    """User login"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        
        return Response(
            {
                'message': 'Login successful',
                'token': token.key,
                'user': UserProfileSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """User logout"""
    try:
        request.user.auth_token.delete()
        return Response(
            {'message': 'Logout successful'},
            status=status.HTTP_200_OK
        )
    except:
        return Response(
            {'error': 'Error logging out'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """Get user dashboard data"""
    user = request.user
    
    # Get user-specific data based on user type
    dashboard_data = {
        'user': UserProfileSerializer(user).data,
        'notifications': [],  # Add notification logic
        'recent_activities': [],  # Add activity logic
    }
    
    if user.user_type == 'donor':
        from donations.models import Donation
        donations = Donation.objects.filter(donor_email=user.email)[:5]
        dashboard_data['recent_donations'] = donations.count()
        dashboard_data['total_donated'] = sum(d.amount for d in donations if d.status == 'completed')
    
    elif user.user_type == 'volunteer':
        from donations.models import Volunteer
        try:
            volunteer = Volunteer.objects.get(email=user.email)
            dashboard_data['volunteer_hours'] = volunteer.hours_contributed
            dashboard_data['projects_participated'] = volunteer.projects_participated
        except Volunteer.DoesNotExist:
            pass
    
    elif user.user_type == 'beneficiary':
        from programs.models import ScholarshipApplication
        applications = ScholarshipApplication.objects.filter(email=user.email)
        dashboard_data['scholarship_applications'] = applications.count()
        dashboard_data['approved_scholarships'] = applications.filter(status='approved').count()
    
    return Response(dashboard_data, status=status.HTTP_200_OK)
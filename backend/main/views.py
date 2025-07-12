from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        # Get the data from request
        data = request.data.copy()
        
        # Hash the password if it exists
        if 'password_hash' in data:
            data['password_hash'] = make_password(data['password_hash'])
        
        # Create serializer with modified data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return response without password
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data.copy()
        response_data.pop('password', None)
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class ViolationViewSet(viewsets.ModelViewSet):
    queryset = Violation.objects.all()
    serializer_class = ViolationSerializer

class HubViewSet(viewsets.ModelViewSet):
    queryset = Hub.objects.all()
    serializer_class = HubSerializer

class VehicleDocumentViewSet(viewsets.ModelViewSet):
    queryset = VehicleDocument.objects.all()
    serializer_class = VehicleDocumentSerializer

class VehicleRouteLogViewSet(viewsets.ModelViewSet):
    queryset = VehicleRouteLog.objects.all()
    serializer_class = VehicleRouteLogSerializer

class ScanLogViewSet(viewsets.ModelViewSet):
    queryset = ScanLog.objects.all()
    serializer_class = ScanLogSerializer

class HubLogViewSet(viewsets.ModelViewSet):
    queryset = HubLog.objects.all()
    serializer_class = HubLogSerializer

@csrf_exempt
@api_view(['POST'])
def login(request):
    print("Received login request:", request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        print(f"Checking for user {username} in database.")
        user = User.objects.filter(name=username).first()
        if user:
            print(f"User {username} found in database. Checking password hash.")
            if check_password(password, user.password_hash):
                print(f"User {username} logged in successfully.")
                serializer = UserSerializer(user)
                return Response(serializer.data)
            print(f"Password hash for user {username} did not match.")
        print(f"User {username} not found in database.")
    print("Login request failed. Returning 401.")
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def CameraDetail(request, camID):
    try:
        violations = Violation.objects.filter(cam=camID)
        count = violations.count()
        return Response({'camID': camID, 'count': count})
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def ViolationDetail(request, camID):
    try:
        violations = Violation.objects.filter(cam=camID)
        serializer = ViolationSerializer(violations, many=True)
        return Response(serializer.data)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def VehicleDetail(request, chipID):
    try:
        vehicle = Vehicle.objects.get(chip_id=chipID)
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)
    except Vehicle.DoesNotExist:
        return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
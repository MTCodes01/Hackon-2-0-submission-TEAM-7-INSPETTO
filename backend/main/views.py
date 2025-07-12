from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        # Get the data from request
        data = request.data.copy()
        
        # Hash the password if it exists
        if 'password' in data:
            data['password'] = make_password(data['password'])
        
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

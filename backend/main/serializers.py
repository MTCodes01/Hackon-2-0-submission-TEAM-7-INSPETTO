from rest_framework import serializers
from .models import User, Camera, Hub, Vehicle, Violation, VehicleDocument, VehicleRouteLog, ScanLog, HubLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = '__all__'

class HubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = '__all__'

class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleDocument
        fields = '__all__'

class VehicleRouteLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleRouteLog
        fields = '__all__'

class ScanLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanLog
        fields = '__all__'

class HubLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubLog
        fields = '__all__'

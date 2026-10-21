from rest_framework import serializers
from django.contrib.auth.models import User
from service_requests.models import ServiceRequestModel

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]

class ServiceRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model=ServiceRequestModel
        fields="__all__"
        read_only_fields=["id","created_at","owner"]

def validate_vehicle_number(self, value):
    if len(value) < 9:
        raise serializers.ValidationError("Vehicle number is too short")
    return value


def validate_problem_description(self, value):
    if len(value) < 10:
        raise serializers.ValidationError("Description must contain at least 10 characters")
    return value

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Service, ServiceMedia, ServiceAvailability, Discount


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ['user', 'created_at']


class ServiceMediaSerializer(ModelSerializer):
    class Meta:
        model = ServiceMedia
        fields = "__all__"


class ServiceAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAvailability
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
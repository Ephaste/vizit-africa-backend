from rest_framework import serializers
from .models import BookingItem, Booking
from datetime import date

class BookingItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = BookingItem
        fields = [
            'id', 'service', 'start_date', 'end_date', 'quantity', 
            'unit_price', 'subtotal', 'status', 'created_at'
        ]
        read_only_fields = ['subtotal', 'created_at']
    
    def validate(self, data):
        if data['start_date'] < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data

class BookingSerializer(serializers.ModelSerializer):
    items = BookingItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'total_amount', 'currency', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['total_amount', 'created_at', 'updated_at']
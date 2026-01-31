from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='booking.id', read_only=True)
    payment_id = serializers.IntegerField(source='payment.id', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'booking_id', 'payment_id', 'pdf_url', 'qr_code_data', 'issued_at', 'expires_at']
        read_only_fields = ['issued_at', 'expires_at']

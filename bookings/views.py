from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import BookingItem, Booking
from .serializers import BookingItemSerializer, BookingSerializer
# Tickets related imports
from rest_framework.decorators import api_view
from tickets.models import Ticket
from tickets.serializers import TicketSerializer
from tickets.utils import generate_qr_code, generate_ticket_pdf
from django.http import HttpResponse, Http404
from django.core.files.storage import default_storage
import os
from django.utils import timezone
#Transactions import
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from decimal import Decimal



class CreateBookingItemView(generics.CreateAPIView):
    serializer_class = BookingItemSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateBookingItemView(generics.UpdateAPIView):
    serializer_class = BookingItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BookingItem.objects.filter(user=self.request.user, status='draft')

class BookingItemListView(generics.ListAPIView):
    serializer_class = BookingItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BookingItem.objects.filter(user=self.request.user, status='draft')

class ConfirmBookingView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            draft_items = BookingItem.objects.filter(user=request.user, status='draft')
            
            if not draft_items.exists():
                return Response(
                    {'error': 'No draft booking items found'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                total_amount=sum(item.subtotal for item in draft_items),
                currency='USD'
            )
            
            # Update items
            draft_items.update(booking=booking, status='reserved')
            
            serializer = self.get_serializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': 'Failed to create booking'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    


@api_view(['POST'])
def generate_ticket(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user, status='confirmed')
        
        # Check if booking has payment
        if not hasattr(booking, 'payments') or not booking.payments.filter(status='succeeded').exists():
            return Response({'error': 'No successful payment found'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment = booking.payments.filter(status='succeeded').first()
        
        # Check if ticket already exists
        if hasattr(booking, 'ticket'):
            serializer = TicketSerializer(booking.ticket)
            return Response(serializer.data)
        
        # Generate QR code data
        qr_data = f"VZT-{booking.id}-{payment.id}-{booking.user.id}"
        qr_code = generate_qr_code(qr_data)
        
        # Create ticket
        ticket = Ticket.objects.create(
            booking=booking,
            payment=payment,
            qr_code_data=qr_code
        )
        
        # Generate PDF
        pdf_path = generate_ticket_pdf(ticket)
        ticket.pdf_url = request.build_absolute_uri(f"/media/{pdf_path}")
        ticket.save()
        
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def download_ticket(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        
        if not hasattr(booking, 'ticket'):
            return Response({'error': 'No ticket found for this booking'}, status=status.HTTP_404_NOT_FOUND)
        
        ticket = booking.ticket
        if not ticket.pdf_url:
            return Response({'error': 'Ticket PDF not generated yet'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract file path from URL safely
        try:
            pdf_path = ticket.pdf_url.split('/media/')[-1]
        except (IndexError, AttributeError):
            return Response({'error': 'Invalid ticket URL'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_storage.exists(pdf_path):
            return Response({'error': 'Ticket file not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serve the file
        try:
            file_content = default_storage.open(pdf_path).read()
            response = HttpResponse(file_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
            return response
        except Exception:
            return Response({'error': 'Failed to read ticket file'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def verify_ticket(request):
    qr_data = request.data.get('qr_code_data')
    
    if not qr_data:
        return Response({'error': 'QR code data required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ticket = Ticket.objects.get(qr_code_data=qr_data)
        
        # Check if ticket is expired
        from django.utils import timezone
        if ticket.expires_at < timezone.now():
            return Response({
                'valid': False,
                'message': 'Ticket has expired'
            }, status=status.HTTP_200_OK)
        
        # Check booking status
        if ticket.booking.status != 'confirmed':
            return Response({
                'valid': False,
                'message': 'Booking not confirmed'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'valid': True,
            'ticket_id': ticket.id,
            'booking_id': ticket.booking.id,
            'user': ticket.booking.user.get_full_name() or ticket.booking.user.username,
            'total_amount': ticket.booking.total_amount,
            'currency': ticket.booking.currency,
            'issued_at': ticket.issued_at,
            'expires_at': ticket.expires_at
        }, status=status.HTTP_200_OK)
        
    except Ticket.DoesNotExist:
        return Response({
            'valid': False,
            'message': 'Invalid ticket'
        }, status=status.HTTP_200_OK)




@api_view(['POST'])
def process_commission(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, status='confirmed')
        
        # Check if commission already processed
        if Transaction.objects.filter(booking=booking, transaction_type='commission').exists():
            return Response({'message': 'Commission already processed'}, status=status.HTTP_200_OK)
        
        # Calculate commission (10% of total amount)
        commission_rate = Decimal('0.10')
        commission_amount = booking.total_amount * commission_rate
        
        # Create commission transaction
        transaction = Transaction.objects.create(
            booking=booking,
            user=booking.user,
            amount=commission_amount,
            currency=booking.currency,
            transaction_type='commission',
            status='completed'
        )
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': 'Failed to process commission'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    
    # Filter by type if provided
    transaction_type = request.query_params.get('type')
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def process_refund(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        
        if booking.status != 'confirmed':
            return Response({'error': 'Only confirmed bookings can be refunded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already refunded
        if Transaction.objects.filter(booking=booking, transaction_type='refund').exists():
            return Response({'error': 'Booking already refunded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create refund transaction
        transaction = Transaction.objects.create(
            booking=booking,
            user=booking.user,
            amount=booking.total_amount,
            currency=booking.currency,
            transaction_type='refund',
            status='pending'
        )
        
        # Update booking status
        booking.status = 'cancelled'
        booking.save()
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def process_payout(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, status='confirmed')
        
        # Get the service owner (vendor) from booking items
        booking_items = booking.items.all()
        if not booking_items.exists():
            return Response({'error': 'No booking items found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Assuming all items in a booking belong to the same vendor
        vendor = booking_items.first().service.user
        
        # Check if payout already processed
        if Transaction.objects.filter(booking=booking, transaction_type='payout').exists():
            return Response({'message': 'Payout already processed'}, status=status.HTTP_200_OK)
        
        # Calculate payout (90% of total amount - after 10% commission)
        commission_rate = Decimal('0.10')
        payout_amount = booking.total_amount * (Decimal('1.00') - commission_rate)
        
        # Create payout transaction
        transaction = Transaction.objects.create(
            booking=booking,
            user=vendor,  # Payout goes to vendor
            amount=payout_amount,
            currency=booking.currency,
            transaction_type='payout',
            status='completed'
        )
        
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def vendor_payouts(request):
    """Get all payouts for the current vendor"""
    payouts = Transaction.objects.filter(
        user=request.user, 
        transaction_type='payout'
    )
    
    # Filter by status if provided
    status_filter = request.query_params.get('status')
    if status_filter:
        payouts = payouts.filter(status=status_filter)
    
    serializer = TransactionSerializer(payouts, many=True)
    return Response(serializer.data)

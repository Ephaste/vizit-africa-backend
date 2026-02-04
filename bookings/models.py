from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class BookingItem(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('reserved', 'Reserved'), 
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='booking_items')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='service_bookings')
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        try:
            if self.unit_price and self.quantity:
                self.subtotal = self.unit_price * self.quantity
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValueError(f"Error saving booking item: {str(e)}")

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    # def calculate_total(self):
    #     return sum(item.subtotal for item in self.items.all())
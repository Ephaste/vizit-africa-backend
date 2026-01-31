from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class BookingItem(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('reserved', 'Reserved'), 
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_items')
    service_id = models.PositiveIntegerField()
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
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def calculate_total(self):
        return sum(item.subtotal for item in self.items.all())
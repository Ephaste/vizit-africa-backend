from django.contrib import admin
from .models import BookingItem, Booking

@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'service_id', 'quantity', 'subtotal', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'service_id']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']
from django.urls import path
from .views import (
    CreateBookingItemView, UpdateBookingItemView, BookingItemListView,
    ConfirmBookingView, BookingListView, BookingDetailView, generate_ticket
)

urlpatterns = [
    # Booking Items (Cart)
    path('items/', BookingItemListView.as_view(), name='booking-items-list'),
    path('items/create/', CreateBookingItemView.as_view(), name='create-booking-item'),
    path('items/<int:pk>/update/', UpdateBookingItemView.as_view(), name='update-booking-item'),
    
    # Bookings
    path('confirm/', ConfirmBookingView.as_view(), name='confirm-booking'),
    path('', BookingListView.as_view(), name='bookings-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),

    # Ticket Generation
    path('<int:booking_id>/generate-ticket/', generate_ticket, name='generate-ticket'),
]
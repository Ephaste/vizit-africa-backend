from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Service, ServiceMedia, ServiceAvailability, Discount
from .serializers import ServiceSerializer, ServiceMediaSerializer, ServiceAvailabilitySerializer, DiscountSerializer
from .permissions import IsApprovedVendor

class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated(), IsApprovedVendor()]

    def get_queryset(self):
        if self.action == 'list' or self.action == 'retrieve':
            return Service.objects.filter(status='active')
        return Service.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ServiceMediaViewSet(ModelViewSet):
    serializer_class = ServiceMediaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ServiceMedia.objects.filter(service__user=self.request.user) 


class ServiceAvailabilityViewSet(ModelViewSet):
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ServiceAvailability.objects.filter(service__user=self.request.user)


class DiscountViewSet(ModelViewSet):
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'vendor'):
            return Discount.objects.filter(vendor=user.vendor) | Discount.objects.filter(vendor__isnull=True)
        return Discount.objects.filter(vendor__isnull=True)
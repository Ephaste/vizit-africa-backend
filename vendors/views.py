from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Vendor
from .serializers import VendorSerializer
from .permissions import IsVendorOwner


# Create your views here.
class VendorViewSet(ModelViewSet):
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsVendorOwner]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Vendor.objects.all()
        return Vendor.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


        #admin approval endpoint

    class VendorViewSet(ModelViewSet):
        ...

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        vendor = self.get_object()
        vendor.is_approved = True
        vendor.approved_by = request.user
        vendor.approved_on = now()
        vendor.save()
        return Response({"status": "Vendor approved"})

from rest_framework.serializers import ModelSerializer
from .models import Vendor


class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"
        read_only_fields = ['is_approved', 'approved_by', 'approved_on', 'user']
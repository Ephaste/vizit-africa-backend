from django.db import models
from django.conf import settings

class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    vendor_type = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="approved_vendors")
    approved_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.business_name} ({self.vendor_type})"
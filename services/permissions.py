from rest_framework.permissions import BasePermission

class IsApprovedVendor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'vendor') and request.user.vendor.is_approved

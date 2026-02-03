from rest_framework.permissions import BasePermission
from accounts.models import User

class IsAdmin(BasePermission):
    message = "Only admin can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )

class IsVendor(BasePermission):
    message = "Only vendor can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "vendor"
        )

class IsTourist(BasePermission):
    message = "Only tourist can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "tourist"
        )

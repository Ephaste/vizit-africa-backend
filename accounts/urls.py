from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet, LoginViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),

    # JWT auth (DO NOT use router)
    path("login/", LoginViewSet.as_view(), name="login"),
]

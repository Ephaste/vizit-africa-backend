from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.serializers import (
    UserRegisterSerializer,
    VerifyEmailSerializer,
    CustomTokenObtainPairSerializer,
)
from accounts.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    Endpoints:
    - POST /api/accounts/users/           → Register
    - GET  /api/accounts/users/           → List users (admin)
    - GET  /api/accounts/users/profile/   → Logged-in profile
    - POST /api/accounts/users/verify_email/ → Activate account
    """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        if self.action == "list":
            return [IsAdmin()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().only(
            "id", "full_name", "email", "role", "created_at"
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def verify_email(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        verification = serializer.validated_data["verification"]

        user.is_active = True
        user.save()

        verification.is_used = True
        verification.save()

        return Response(
            {"message": "Account activated successfully"},
            status=status.HTTP_200_OK,
        )


class LoginViewSet(TokenObtainPairView):
    """
    POST /api/accounts/login/
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

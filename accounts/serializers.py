from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "phone_number",
            "bio",
            "role",
            "preferred_currency",
            "password",
            "re_password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        re_password = attrs.get("re_password")
        
        if not password or not re_password:
            raise serializers.ValidationError(
                {"password": "Password fields are required"}
            )
            
        if password != re_password:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password")

        user = User.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            full_name=validated_data.get("full_name"),
            phone_number=validated_data.get("phone_number"),
            bio=validated_data.get("bio", ""),
            role=validated_data.get("role", User.CLIENT),

            preferred_currency=validated_data.get("preferred_currency", "USD"),
        )
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer to include user details in login response
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["id"] = str(user.id)
        token["email"] = user.email
        token["role"] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "full_name": self.user.full_name,
            "email": self.user.email,
            "phone_number": self.user.phone_number,
            "role": self.user.role,
            "preferred_currency": self.user.preferred_currency,
        }

        return data

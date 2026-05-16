from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name", "role"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_role(self, value):
        request = self.context.get("request")
        requester = getattr(request, "user", None)
        requester_role = getattr(requester, "role", None)

        if value in {"admin", "manager"} and requester_role != "admin":
            raise serializers.ValidationError("Only admins can create admin or manager users")

        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "is_staff",
            "date_joined"
        ]
        read_only_fields = ["id", "date_joined", "is_staff"]

from django.http import Http404
from rest_framework import serializers

from .models import User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "bio",
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError()
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    confirmation_code = serializers.UUIDField()

    class Meta:
        model = User
        fields = ("confirmation_code", "username")

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            return value
        raise Http404

from .models import User, Subscription
from services.functions import (
    is_subscribed,
    validate_current_user_password,
    save_new_user_password
)

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


class GETUserSerializer(serializers.ModelSerializer):
    def to_representation(self, user: User) -> dict:
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_subscribed': is_subscribed(
                user=user, request=self.context['request']
            )
        }

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class POSTUserSerializer(serializers.ModelSerializer):
    def to_representation(self, user: User) -> User:
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
        }


class UserPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, password: str) -> str:
        return validate_current_user_password(
            user=self.context['request'].user,
            password=password
        )

    def validate_new_password(self, password: str) -> str:
        validate_password(password=password)
        return password

    def save(self, **kwargs: dict) -> User:
        return save_new_user_password(
            user=self.context['request'].user,
            password=self.validated_data['new_password']
        )

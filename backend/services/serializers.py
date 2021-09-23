from django.contrib.auth.models import update_last_login

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    """Custom TokenObtainPairSerializer with modified <validate> method,
    which just pass attrs to parent, not adding new extra fields to data.
    """
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        return super().validate(attrs)


class TokenSerializer(CustomTokenObtainPairSerializer):
    """Custom TokenSerializer, which validates request and returns
    a dict named <data> with an auth token.
    """
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['auth_token'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

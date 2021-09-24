from .serializers import TokenSerializer

from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainView(TokenObtainPairView):
    """Custom TokenObtainPairView, which returns only authentication token,
    but not refresh one.
    """
    serializer_class = TokenSerializer

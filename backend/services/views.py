from services.serializers import CustomAuthTokenSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthTokenView(ObtainAuthToken):
    """Custom Auth Token View for login and logout. Uses custom serializers,
    in order to do authentication by email, not username.
    """
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        if 'login/' in request.path:
            serializer = self.serializer_class(
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)

            token, _ = Token.objects.get_or_create(
                user=serializer.validated_data['user']
            )
            return Response(data={'auth_token': token.key})

        if not request.user.is_authenticated:
            return Response(
                data={
                    'success': False,
                    'message': 'Authentication credentials were not provided.'
                }
            )

        request.user.auth_token.delete()

        return Response(
            data={
                'success': True,
                'message': 'Authentication token was sucessfully deleted.'
            }
        )

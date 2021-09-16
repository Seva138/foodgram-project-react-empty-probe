from .models import User
from .serializers import (
    GETUserSerializer,
    POSTUserSerializer,
    UserPasswordSerializer
)
from services.functions import are_proper_credentials, get_access_token

from rest_framework import views, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class CustomTokenObtainView(views.APIView):
    """Token-obtain view, which accepts unique email address and password --
    returns a json with a token, providing the given credentials are corrent.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        if are_proper_credentials(request=request):
            # TODO: email field should be unique one.
            return Response(
                data=get_access_token(),
                status=status.HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """List & Retrieve View Set for User model. Uses POSTUserSerializer
    for accout registration, otherwise GETUserSerializer.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = GETUserSerializer
        else:
            serializer_class = POSTUserSerializer

        return serializer_class


class UserDetailView(generics.RetrieveAPIView):
    """
    Retrieve API View for users/me/ endpoint --
    shows account information about authenticated request.user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = GETUserSerializer

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordView(generics.CreateAPIView):
    """
    Create API View, which accepts a current password and a new password --
    as a result, sets the new password if validation process was successfull.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

from .models import User
from .serializers import (
    GETUserSerializer,
    POSTUserSerializer,
    UserPasswordSerializer
)
from services.functions import (
        are_proper_credentials, get_user, get_access_token
)

from rest_framework import views, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class CustomTokenObtainView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if are_proper_credentials(request=request):
            return Response(
                data=get_access_token(),
                status=status.HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = GETUserSerializer
        else:
            serializer_class = POSTUserSerializer

        return serializer_class


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GETUserSerializer

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

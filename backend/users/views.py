from .models import User
from .serializers import (
    GETUserSerializer,
    POSTUserSerializer,
    UserPasswordSerializer,
    UserSubscriptionSerializer
)

from rest_framework import views, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """List & Retrieve Model View Set for User model. Uses POSTUserSerializer
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
    """Retrieve API View for users/me/ endpoint --
    shows account information for authenticated request.user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = GETUserSerializer

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordView(generics.CreateAPIView):
    """Create API View, which accepts a current password and a new password --
    as a result, sets the new password if validation process was successfull.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionView(viewsets.ViewSet):
    """View Set for user-to-user subscription process.
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = request.user.subscriptions.all()
        serializer = UserSubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, id):
        serializer = UserSubscriptionSerializer(request.user)
        serializer.validate(request=request, id=id)
        return Response(serializer.create(request=request, id=id))

    def destroy(self, request, id):
        serializer = UserSubscriptionSerializer(request.user)
        serializer.validate(request=request, id=id)
        serializer.destroy(request=request, id=id) 
        return Response(status=status.HTTP_204_NO_CONTENT)

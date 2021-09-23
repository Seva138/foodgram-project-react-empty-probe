from .models import Recipe, Tag, Ingredient
from .serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
)
from .permissions import RecipePermission
from users.serializers import (
    UserFavoriteRecipeSerializer,
    UserShoppingCartSerializer
)
from users.models import UserCart
from services.functions import return_ingredients

from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (RecipePermission,)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class TagViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, id=id)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        queryset = Ingredient.objects.all()
        tag = get_object_or_404(queryset, id=id)
        serializer = IngredientSerializer(tag)
        return Response(serializer.data)


class UserFavoriteRecipeViewSet(viewsets.ViewSet):
    permissions_classes = (IsAuthenticated,)

    def create(self, request, id):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, id=id)
        serializer = FavoriteRecipeSerializer(recipe)
        serializer.validate(request=request, id=id)
        serializer.create(request=request, id=id)
        return Response(serializer.data)

    def destroy(self, request, id):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, id=id)
        serializer = FavoriteRecipeSerializer(recipe)
        serializer.validate(request=request, id=id)
        serializer.destroy(request=request, id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserShoppingCartViewSet(viewsets.ViewSet):
    permissions_classes = (IsAuthenticated,)

    def create(self, request, id):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, id=id)
        serializer = UserShoppingCartSerializer(recipe)
        serializer.validate(request=request, id=id)
        serializer.create(request=request, id=id)
        return Response(serializer.data)

    def destroy(self, request, id):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, id=id)
        serializer = UserShoppingCartSerializer(recipe)
        serializer.validate(request=request, id=id)
        serializer.destroy(request=request, id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartView(views.APIView):
    def get(self, request):
        try:
            return FileResponse(
                open(return_ingredients(request=request).name, mode='rb'),
                as_attachment=True,
                status=200
            )
        except AttributeError as e:
            return HttpResponse(
                'You have to authorize in order to download shopping cart.',
                status=401
            )
        except ObjectDoesNotExist as e:
            return HttpResponse(
                'You do not have a shopping cart on your account.',
                status=400
            )
        except FileNotFoundError as e: 
            return HttpResponse(
                'We have some troubles, please, try later.',
                status=500
            )

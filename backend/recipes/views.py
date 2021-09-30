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
from services.functions import get_recipe_queryset, load_ingredients
from services.pagination import CustomPageNumberPagination

from django.shortcuts import get_object_or_404
from django.http import FileResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (RecipePermission,)
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return get_recipe_queryset(self)

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('tags', 'author')


class TagViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, id=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Ingredient.objects.all()
        tag = get_object_or_404(queryset, id=pk)
        serializer = IngredientSerializer(tag)
        return Response(serializer.data)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class UserFavoriteRecipeViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, id):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, id=id)
        serializer = UserFavoriteRecipeSerializer(recipe)
        serializer.validate(request=request, id=id)
        serializer.create(request=request, id=id)
        return Response(serializer.data)

    def destroy(self, request, id):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, id=id)
        serializer = UserFavoriteRecipeSerializer(recipe)
        serializer.validate(request=request, id=id)
        serializer.destroy(request=request, id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserShoppingCartViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

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
            with open(file=f'{request.user.shopping_cart.id}_SC.txt',
                    mode='w+') as file:
                load_ingredients(request=request, file=file)

            return FileResponse(
                open(file=f'{request.user.shopping_cart.id}_SC.txt',
                    mode='rb'),
                as_attachment=True,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return JsonResponse(
                data={'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

from .models import UserSubscription
from recipes.models import Recipe
from services.functions import (
    is_subscribed,

    create_user,
    validate_current_user_password,
    save_new_user_password,

    create_subscription,
    destroy_subscription,
    validate_subscription,

    create_favorite_recipe,
    destroy_favorite_recipe,
    validate_favorite_recipe_process,

    add_recipe_into_user_shopping_cart,
    destroy_recipe_from_user_shopping_cart,
    validate_user_shopping_cart_process
)

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.request import Request


User = get_user_model()


class GETUserSerializer(serializers.ModelSerializer):
    def to_representation(self, user: User) -> dict:
        return {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,

            'is_subscribed': is_subscribed(
                user=user,
                request=self.context['request']
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

    def create(self, validated_data: dict) -> User:
        return create_user(validated_data=validated_data)

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

    def save(self) -> User:
        return save_new_user_password(
            user=self.context['request'].user,
            password=self.validated_data['new_password']
        )


class NestedUserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscriptionSerializer(serializers.ModelSerializer):
    def to_representation(self, user: User):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit'
        )

        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,

            'recipes': NestedUserRecipeSerializer(
                user.recipes.all()[recipes_limit] if recipes_limit \
                    else user.recipes.all(),
                many=True
            ).data,

            'recipes_count': user.recipes.all().count(),
            'is_subscribed': True,
        }

    def validate(self, request: Request, id: int) -> dict:
        validate_subscription(request=request, id=id)

    def create(self, request: Request, id: int) -> User:
        return self.to_representation(
            create_subscription(request=request, id=id)
        )

    def destroy(self, request: Request, id: int) -> None:
        return destroy_subscription(request=request, id=id)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserFavoriteRecipeSerializer(serializers.ModelSerializer):
    def to_representation(self, recipe: Recipe):
        return {
            'id': recipe.id,
            'name': recipe.name,
            'image': recipe.image.url if recipe.image else None,
            'cooking_time': recipe.cooking_time
        }

    def create(self, request: Request, id: int) -> Recipe:
        return create_favorite_recipe(request=request, id=id)

    def destroy(self, request: Request, id: int) -> None:
        return destroy_favorite_recipe(request=request, id=id)

    def validate(self, request: Request, id: int) -> None:
        return validate_favorite_recipe_process(request, id)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserShoppingCartSerializer(serializers.ModelSerializer):
    def to_representation(self, recipe: Recipe):
        return {
            'id': recipe.id,
            'name': recipe.name,
            'image': recipe.image.url if recipe.image else None,
            'cooking_time': recipe.cooking_time
        }

    def create(self, request: Request, id: int) -> Recipe:
        return add_recipe_into_user_shopping_cart(request=request, id=id)

    def destroy(self, request: Request, id: int) -> None:
        return destroy_recipe_from_user_shopping_cart(request=request, id=id)

    def validate(self, request: Request, id: int) -> None:
        return validate_user_shopping_cart_process(request, id)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

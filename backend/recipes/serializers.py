from .models import Recipe, Ingredient, Tag, RecipeIngredient, User
from users.serializers import GETUserSerializer
from services.serializer_fields import (
    Base64ToContentFileField,
    HEXToColourNameField
)
from services.functions import (
    create_recipe,
    update_recipe,
    is_favorited,
    is_in_shopping_cart,
)

from rest_framework import serializers
from rest_framework.request import Request


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ToContentFileField()
    ingredients = serializers.JSONField()

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        read_only=False
    )

    def to_representation(self, recipe: Recipe) -> dict:
        return {
            'id': recipe.id,
            'name': recipe.name,
            'image': recipe.image.url if recipe.image else None,
            'text': recipe.text,
            'cooking_time': recipe.cooking_time,
            'tags': TagSerializer(recipe.tags, many=True).data,


            'author': GETUserSerializer(
                recipe.author,
                context={'request': self.context['request']}
            ).data,

            'ingredients': RecipeIngredientSerializer(
                RecipeIngredient.objects.filter(recipe=recipe),
                many=True
            ).data,

            'is_favorited': is_favorited(
                recipe=recipe,
                request=self.context['request']
            ),

            'is_in_shopping_cart': is_in_shopping_cart(
                recipe=recipe,
                request=self.context['request']
            )
        }

    def create(self, validated_data: dict) -> Recipe:
        return create_recipe(
            validated_data=validated_data,
            request=self.context['request']
        )

    def update(self, instance: Recipe, validated_data: dict) -> Recipe:
        return update_recipe(instance=instance, validated_data=validated_data)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
        )
        extra_kwargs = {
            'id': {'required': False},
            'author': {'required': False},
            'name': {'required': True},
            'image': {'required': True},
            'text': {'required': True},
            'ingredients': {'required': True},
            'tags': {'required': True},
            'cooking_time': {'required': True},
        }


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    color = HEXToColourNameField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    def to_representation(self, recipe_ingredient: RecipeIngredient) -> dict:
        return {
            'id': recipe_ingredient.ingredient.id,
            'name': recipe_ingredient.ingredient.name,
            'measurement_unit': recipe_ingredient.ingredient.measurement_unit,
            'amount': recipe_ingredient.amount
        }

    class Meta:
        model = RecipeIngredient
        exclude = ('recipe',)

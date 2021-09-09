from .models import Recipe, Ingredient, Tag, RecipeIngredient, User
from services.serializer_fields import (
    Base64ToContentFileField,
    HEXToColourNameField
)
from services.functions import create_recipe
from rest_framework import serializers


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


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    colour = HEXToColourNameField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'colour', 'slug')



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
            'author': 'author',
            'name': recipe.name,
            'image': recipe.image.url,
            'text': recipe.text,
            'cooking_time': recipe.cooking_time,
            'ingredients': RecipeIngredientSerializer(
                RecipeIngredient.objects.filter(recipe=recipe),
                many=True
            ).data,
            'tags': TagSerializer(recipe.tags, many=True).data
        }

    def create(self, validated_data: dict) -> Recipe:
        return create_recipe(validated_data: dict) -> Recipe

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

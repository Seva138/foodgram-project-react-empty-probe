from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipies',
        verbose_name='Author of a recipe'
    )

    name = models.CharField(max_length=200, verbose_name='Name of a recipe')
    image = models.ImageField(upload_to='images/%Y-%m-%d')
    text = models.TextField(verbose_name='Description of a recipe')

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='Ingredients of a recipe'
    )

    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        verbose_name='Tags of a recipe'
    )

    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(44640)
        ],
        verbose_name='Cooking time in minutes'
    )

    creation_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Date of creation'
    )


class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name='Name of a tag')
    colour = models.CharField(max_length=64, verbose_name='Colour of a tag')
    slug = models.SlugField(max_length=64, verbose_name='Slug of a tag')


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Name of an ingredient'
    )

    measurement_unit = models.CharField(max_length=32)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE
    )

    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE
    )

    amount = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(44640)
        ],
        verbose_name='Amount of ingredients'
    )


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE
    )

    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE
    )

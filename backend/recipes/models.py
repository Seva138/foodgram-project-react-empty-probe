from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='Author of a recipe.'
    )

    name = models.CharField(max_length=200, help_text='Name of a recipe.')

    image = models.ImageField(
        max_length=4096,
        upload_to='images/%Y-%m-%d',
        help_text='Image of a recipe.'
    )

    text = models.TextField(help_text='Description of a recipe.')

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        help_text='Ingredients of a recipe.'
    )

    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        help_text='Tags of a recipe.'
    )

    cooking_time = models.IntegerField(
        default=60,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(44640)
        ],
        help_text='Cooking time in minutes.'
    )

    creation_date = models.DateTimeField(
        auto_now=True,
        help_text='Date of creation of a recipe.'
    )


class Tag(models.Model):
    name = models.CharField(max_length=256, help_text='Name of a tag.')
    colour = models.CharField(max_length=64, help_text='Colour of a tag.')
    slug = models.SlugField(max_length=64, help_text='Slug of a tag.')


class Ingredient(models.Model):
    name = models.CharField(max_length=256, help_text='Name of an ingredient.')

    measurement_unit = models.CharField(
        max_length=32,
        help_text='Measurement unit of an ingredient.'
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        help_text='Relation to a recipe.'
    )

    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        help_text='Relation to an ingredient.'
    )

    amount = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(44640)
        ],
        help_text='Amount of ingredients.'
    )


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        help_text='Relation to a recipe.'
    )

    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE,
        help_text='Relation to a tag.'
    )

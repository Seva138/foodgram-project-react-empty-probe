from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author',
        help_text='Author of a recipe.'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='name',
        help_text='Name of a recipe.'
    )

    image = models.ImageField(
        max_length=4096,
        upload_to='images/%Y-%m-%d',
        verbose_name='image',
        help_text='Image of a recipe.'
    )

    text = models.TextField(
        verbose_name='text',
        help_text='Description of a recipe.'
    )

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='ingredient',
        help_text='Ingredients of a recipe.'
    )

    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        verbose_name='tag',
        help_text='Tags of a recipe.'
    )

    cooking_time = models.IntegerField(
        default=60,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(44640)
        ),
        verbose_name='cooking time (m)',
        help_text='Cooking time in minutes.'
    )

    creation_date = models.DateTimeField(
        auto_now=True,
        verbose_name='data of creation',
        help_text='Date of creation of a recipe.'
    )

    class Meta:
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def __str__(self):
        return f'Recipe - id: {self.id}, name: {self.name}.'


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='name',
        help_text='Name of a tag.'
    )
    colour = models.CharField(
        max_length=64,
        verbose_name='colour',
        help_text='Colour of a tag.'
    )
    slug = models.SlugField(
        max_length=64,
        verbose_name='slug',
        help_text='Slug of a tag.'
    )

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return f'Tag - id: {self.id}, name: {self.name}.'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='name',
        help_text='Name of an ingredient.'
    )

    measurement_unit = models.CharField(
        max_length=32,
        verbose_name='measurement_unit',
        help_text='Measurement unit of an ingredient.'
    )

    class Meta:
        verbose_name = 'ingrediet'
        verbose_name_plural = 'ingredients'

    def __str__(self):
        return f'Ingredient - id: {self.id}, name: {self.name}.'


class RecipeIngredient(models.Model):
    """Intermediate "join" table for a relation between a recipe
    and an ingredient. Additionaly implements <amount> field.
    """
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='recipe',
        help_text='Relation to a recipe.'
    )

    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='ingredient',
        help_text='Relation to an ingredient.'
    )

    amount = models.IntegerField(
        default=1,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(44640)
        ),
        verbose_name='amount',
        help_text='Amount of ingredients.'
    )

    class Meta:
        verbose_name = 'recipe ingredient relation'
        verbose_name_plural = 'recipe ingredient relations'

    def __str__(self):
        return f'RecipeIngredient - id: {self.id}.'


class RecipeTag(models.Model):
    """Intermediate "join" table for a relation between a recipe and tag.
    """
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='recipe',
        help_text='Relation to a recipe.'
    )

    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE,
        verbose_name='tag',
        help_text='Relation to a tag.'
    )

    class Meta:
        verbose_name = 'recipe tag relation'
        verbose_name_plural = 'recipe tag relations'

    def __str__(self):
        return f'RecipeTag - id: {self.id}.'

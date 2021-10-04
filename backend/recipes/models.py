from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )

    name = models.CharField(
        max_length=200,
        verbose_name='имя',
    )

    image = models.ImageField(
        max_length=4096,
        upload_to='images/%Y-%m-%d',
        verbose_name='фото',
    )

    text = models.TextField(verbose_name='описание')

    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='ингредиет',
    )

    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        verbose_name='тэг',
    )

    cooking_time = models.IntegerField(
        default=60,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(44640)
        ),
        verbose_name='время приготовления (в минутах)',
    )

    creation_date = models.DateTimeField(
        auto_now=True,
        verbose_name='дата создания рецепта',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'


    def __str__(self):
        return f'Рецепт - id: {self.id}, имя: {self.name}.'


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='имя',
    )
    color = models.CharField(
        max_length=64,
        verbose_name='цвет',
    )
    slug = models.SlugField(
        max_length=64,
        verbose_name='слаг',
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return f'Тэг - id: {self.id}, имя: {self.name}.'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='имя',
    )

    measurement_unit = models.CharField(
        max_length=32,
        verbose_name='еденица измерения',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'Игредиент - id: {self.id}, имя: {self.name}.'


class RecipeIngredient(models.Model):
    """Intermediate "join" table for a relation between a recipe
    and an ingredient. Additionaly implements <amount> field.
    """
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='игредиент',
    )

    amount = models.IntegerField(
        default=1,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(44640)
        ),
        verbose_name='количество',
    )

    class Meta:
        verbose_name = 'отношение рецепта к ингредиенту'
        verbose_name_plural = 'отношение рецепта к ингредиентам'

        constraints = (
            models.UniqueConstraint(
                fields=('recipe_id', 'ingredient_id'),
                name='recipe_ingredient_unique_constraint'
            ),
        )

    def __str__(self):
        return f'РецептИнгредиент - id: {self.id}.'


class RecipeTag(models.Model):
    """Intermediate "join" table for a relation between a recipe and tag.
    """
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE,
        verbose_name='тэг',
    )


    class Meta:
        verbose_name = 'отношение рецепта к тэгу'
        verbose_name_plural = 'отношение рецепта к тэгам'

        constraints = (
            models.UniqueConstraint(
                fields=('recipe_id', 'tag_id'),
                name='recipe_tag_unique_constraint'
            ),
        )

    def __str__(self):
        return f'РецептТэг - id: {self.id}.'

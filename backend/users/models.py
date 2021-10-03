from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Extended user model, which uses custom <username> and <email> fields
    along with <subscriptions> & <favorites>. Email field is implemented as
    USERNAME_FIELD for sake of authorization.
    """
    username = models.CharField(
        max_length=150,
        null=True,
        verbose_name='пользователь',
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='электронная почта',
    )

    subscriptions = models.ManyToManyField(
        to='self',
        symmetrical=False,
        through='UserSubscription',
        through_fields=('follower', 'author'),
        verbose_name='подписка на другого пользователя',
    )

    favorites = models.ManyToManyField(
        to='recipes.Recipe',
        through='UserRecipe',
        verbose_name='понравившееся рецепты',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'Пользователь - id: {self.id}, почта: {self.email}.'


class UserCart(models.Model):
    """User's shopping cart, where one can add or delete
    recipes of its choice.
    """
    user = models.OneToOneField(
        to='User',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='пользователь',
    )

    recipes = models.ManyToManyField(
        to='recipes.Recipe',
        verbose_name='рецепт',
    )

    @receiver(post_save, sender=User)
    def create_user_shopping_cart(sender, instance, created, **kwargs):
        if created:
            UserCart.objects.create(user=instance)

    class Meta:
        verbose_name = 'карзина покупок пользователя'
        verbose_name_plural = 'карзина покупок пользователей'

    def __str__(self):
        return f'Карзина - id: {self.id}, владелец: {self.user}.'


class UserSubscription(models.Model):
    """Intermediate "join" table of subscription between two users.
    """
    follower = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        verbose_name='подписчик',
    )

    author = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='автор',
    )

    subscription_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата подписки',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'ПользовательПодписка - id: {self.id}.'



class UserRecipe(models.Model):
    """Intermediate "join" table for user's favorite recipes.
    Additionaly implements <note> field, where user can save some notes.
    """
    user = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='пользователь',
    )

    recipe = models.ForeignKey(
        to='recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    note = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name='примечание',
    )

    class Meta:
        verbose_name = 'отношение пользователя к рецепту'
        verbose_name_plural = 'отношение пользователей к рецептам'

    def __str__(self):
        return f'ПользовательРецепт - id: {self.id}.'

from django.db import models
from django.contrib.auth.models import AbstractUser 


class User(AbstractUser):
    """Extended user model, which uses custom <username> and <email> fields
    along with <subscriptions> & <favorites>. Email field is implemented as
    USERNAME_FIELD for sake of authorization.
    """
    username = models.CharField(
        max_length=150,
        null=True,
        verbose_name='username',
        help_text='User\'s username field.'
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email',
        help_text='User\'s email field.'
    )

    subscriptions = models.ManyToManyField(
        to='self',
        symmetrical=False,
        through='UserSubscription',
        through_fields=('follower', 'author'),
        verbose_name='subscription',
        help_text='User\'s subscriptions to other ones.'
    )

    favorites = models.ManyToManyField(
        to='recipes.Recipe',
        through='UserRecipe',
        verbose_name='favorite',
        help_text='User\'s favorite recipes.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'User - id: {self.id}, email: {self.email}.'



class UserCart(models.Model):
    """User's shopping cart, where one can add or delete
    recipes of its choice.
    """
    user = models.OneToOneField(
        to='User',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='user',
        help_text='Relation to owner of the shopping cart.'
    )

    recipes = models.ManyToManyField(
        to='recipes.Recipe',
        verbose_name='recipe',
        help_text='Relation to a recipe in User\'s shopping cart.'
    )

    class Meta:
        verbose_name = 'user\'s shopping cart'
        verbose_name_plural = 'user\'s shopping carts'

    def __str__(self):
        return f'UserCart - id: {self.id}, owner: {self.user}.'


class UserSubscription(models.Model):
    """Intermediate "join" table of subscription between two users.
    """
    follower = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        verbose_name='follower',
        help_text='Relation to the follower.'
    )

    author = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='author',
        help_text='Relation to the author.'
    )

    subscription_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date of subscription',
        help_text='Date of subscription between two users.'
    )

    class Meta:
        verbose_name = 'user-to-user subscription'
        verbose_name_plural = 'user-to-user subscriptions'

    def __str__(self):
        return f'UserSubscription - id: {self.id}.'



class UserRecipe(models.Model):
    """Intermediate "join" table for user's favorite recipes.
    Additionaly implements <note> field, where user can save some notes.
    """
    user = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='user',
        help_text='User\'s favorite recipes.'
    )

    recipe = models.ForeignKey(
        to='recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='recipe',
        help_text='Recipe that is favorited by user.'
    )

    note = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        verbose_name='note',
        help_text='Note on why user has decided to add a recipe.'
    )

    class Meta:
        verbose_name = 'user recipe relation'
        verbose_name_plural = 'user recipe relations'

    def __str__(self):
        return f'UserRecipe - id: {self.id}.'

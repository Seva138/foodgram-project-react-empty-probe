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
        help_text='User\'s username field.'
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        help_text='User\'s email field.'
    )

    subscriptions = models.ManyToManyField(
        to='self',
        symmetrical=False,
        through='UserSubscription',
        through_fields=('follower', 'author'),
        help_text='User\'s subscriptions to other ones.'
    )

    favorites = models.ManyToManyField(
        to='recipes.Recipe',
        through='UserRecipe',
        help_text='User\'s favorite recipes.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class UserSubscription(models.Model):
    """Intermediate "join" table of subscription between two users.
    Additionaly implements date of creation field.
    """
    follower = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        help_text='Relation to the follower.'
    )

    author = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='followers',
        help_text='Relation to the author.'
    )

    subscription_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Date of subscription between two users.'
    )


class UserRecipe(models.Model):
    """Intermediate "join" table for user's favorite recipes.
    Additionaly implements <note> field, where user can save some notes.
    """
    user = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        help_text='User\'s favorite recipes.'
    )

    recipe = models.ForeignKey(
        to='recipes.Recipe',
        on_delete=models.CASCADE,
        help_text='Recipe that is favorited by user.'
    )

    note = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text='Note on why user has decided to add a recipe.'
    )


class UserCart(models.Model):
    """User's shopping cart, where one can add recipes of its choice.
    """
    user = models.OneToOneField(
        to='User',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        help_text='Relation to owner of the shopping cart.'
    )

    recipes = models.ManyToManyField(
        to='recipes.Recipe',
        help_text='Relation to a recipe in User\'s shopping cart.'
    )

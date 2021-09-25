from users.models import UserSubscription, UserCart
from recipes.models import Recipe, RecipeIngredient
from users.models import UserCart

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, QuerySet

from rest_framework import viewsets, serializers
from rest_framework.request import Request
from rest_framework.permissions import SAFE_METHODS

from typing import Union, List


User = get_user_model()


def load_ingredients(request: Request, file: str) -> None:
    try:
        recipes = request.user.shopping_cart.recipes.all()
        _ = RecipeIngredient.objects.filter(recipe__in=recipes)
        annotated_ingredients = (
            _.values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(Sum('amount'))
        )

        for annotated_ingredient in annotated_ingredients:
            file.write(
                (f"{annotated_ingredient['ingredient__name']}"
                f" - ({annotated_ingredient['ingredient__measurement_unit']})"
                f" - {annotated_ingredient['amount__sum']}.\n")
            )
    except (ObjectDoesNotExist, FileNotFoundError, PermissionError,
        TimeoutError, ProcessLookupError, InterruptedError) as e:
        raise e


def add_ingredients_to_recipe(recipe: Recipe, validated_data: dict) -> None:
    """Adds ingredients with specified amount to a particular recipe,
    using intermediate "join" table RecipeIngredient.
    """
    RecipeIngredient.objects.bulk_create([
        RecipeIngredient(
            recipe=recipe,
            ingredient_id=validated_data['ingredients'][position]['id'],
            amount=validated_data['ingredients'][position]['amount']
        ) for position in range(len(validated_data['ingredients']))
    ])


def create_recipe(validated_data: dict, request: Request) -> Recipe:
    """Creates a recipe and adds the given tags and ingredients to it.
    """
    recipe = Recipe.objects.create(
        author=request.user,
        name=validated_data['name'],
        image=validated_data['image'],
        text=validated_data['text'],
        cooking_time=validated_data['cooking_time']
    )

    recipe.tags.add(*validated_data['tags'])
    add_ingredients_to_recipe(recipe=recipe, validated_data=validated_data)
    return recipe


def update_recipe(instance: Recipe, validated_data: dict) -> Recipe:
    """Entirely updates a particular recipe, rewriting all fields.
    """
    instance.name = validated_data['name']
    instance.image = validated_data['image']
    instance.text = validated_data['text']
    instance.cooking_time = validated_data['cooking_time']

    instance.tags.clear()
    instance.tags.add(*validated_data['tags'])

    instance.ingredients.clear()
    add_ingredients_to_recipe(recipe=instance, validated_data=validated_data)

    instance.save()
    return instance


def is_subscribed(user: User, request: Request) -> bool:
    """Returns True if requested user is subscribed on request.user,
    otherwise False. The same user is considered to be subscribed on itself.
    Returns False for not authorized user.
    """
    try:
        if (request.user.email == user.email
            or UserSubscription.objects.filter(
                   author=request.user,
                   follower=user).exists()):
            return True
        return False
    except AttributeError:
        return False


def is_favorited(recipe: Recipe, request: Request) -> bool:
    """Returns True if a particular recipe is user's favorite one,
    otherwise False. Returns False for not authenticated user.
    """
    try:
        return request.user.favorites.filter(id=recipe.id).exists()
    except AttributeError as e:
        return False


def is_in_shopping_cart(recipe: Recipe, request: Request) -> bool:
    """Returns True if specified recipe is in user's shopping cart,
    otherwise False. Returns False for not authenticated user.
    """
    try:
        return request.user.shopping_cart.recipes.filter(id=recipe.id).exists()
    except (AttributeError, ObjectDoesNotExist) as e:
        return False


def validate_current_user_password(user: User, password: str) -> str:
    """Returns password if specified password is correct,
    otherwise raises validation error.
    """
    if not check_password(
        password=password,
        encoded=user.password):
        raise serializers.ValidationError(
            'Specified current password is wrong.'
        )
    return password


def save_new_user_password(user: User, password: str) -> User:
    """Sets password to a particular user.
    """
    user.set_password(password)
    user.save()
    return user


def create_subscription(request: Request, id: int) -> User:
    """Creates subscription between two authorized users.
    """
    requested_user = User.objects.get(id=id)
    request.user.subscriptions.add(requested_user)
    return requested_user


def destroy_subscription(request: Request, id: int) -> None:
    """Destroys subscription between two authorized users.
    """
    User.objects.get(id=request.user.id).subscriptions.remove(
        User.objects.get(id=id)
    )


def validate_subscription(request: Request, id: int) -> None:
    """Validates subscription process, when user is trying
    to subscribe or unsubscribe.
    """
    if not User.objects.filter(id=id).exists():
        raise serializers.ValidationError('Specified user does not exist.')

    if request.user.id == id:
        raise serializers.ValidationError(
            'You cannot subscribe/unsubscribe on/from yourself.'
        )

    if request.method == 'GET':
        if id in request.user.subscriptions.all().values_list('id', flat=True):
            raise serializers.ValidationError(
                'You cannot subscribe on a user twice.'
            )
    else:
        if id not in User.objects.get(id=request.user.id).subscriptions \
            .values_list('id', flat=True):
            raise serializers.ValidationError(
                'You are not subscribed on this user.'
            )


def create_favorite_recipe(request: Request, id: int) -> Recipe:
    """Creates a favorite recipe for a particular user.
    """
    requested_recipe = Recipe.objects.get(id=id)
    request.user.favorites.add(requested_recipe)
    return requested_recipe


def destroy_favorite_recipe(request: Request, id: int) -> None:
    """Destroys a favorite recipe for a particular user.
    """
    request.user.favorites.remove(Recipe.objects.get(id=id))


def validate_favorite_recipe_process(request: Request, id: int) -> None:
    """Validates a creation or destraction of the favorite recipe,
    when user is trying to create or destroy a favorite one.
    """
    if request.method == 'GET':
        if id in request.user.favorites.all().values_list('id', flat=True):
            raise serializers.ValidationError(
                'You cannot add a recipe twice.'
            )
    else:
        if id not in request.user.favorites.all().values_list('id', flat=True):
            raise serializers.ValidationError(
                'You do not have specified recipe in your favorites.'
            )


def add_recipe_into_user_shopping_cart(request: Request, id: int) -> None:
    """Adds a recipe into a shopping cart of a particular user.
    """
    user_shopping_cart, _ = UserCart.objects.get_or_create(user=request.user)
    user_shopping_cart.recipes.add(Recipe.objects.get(id=id))


def destroy_recipe_from_user_shopping_cart(request: Request, id: int) -> None:
    """Destroys a recipe from a shopping cart of a particular user.
    """
    user_shopping_cart = UserCart.objects.get(user=request.user)
    user_shopping_cart.recipes.remove(Recipe.objects.get(id=id))


def validate_user_shopping_cart_process(request: Request, id: int) -> None:
    """Validates an addition/destruction of a recipe into/from a shopping cart.
    """
    if request.method == 'GET':
        if UserCart.objects.filter(user=request.user).exists():
            if id in UserCart.objects.get(user=request.user).recipes.all() \
                .values_list('id', flat=True):
                raise serializers.ValidationError(
                    'You cannot add a recipe into your shopping cart twice.'
                )
        else:
            # We do not want to validate user's GET request
            # If it was the first one.
            return
    else:
        if not UserCart.objects.filter(user=request.user).exists():
            raise serializers.ValidationError(
                ('You do not have a shopping cart currently, '
                 'so you cannot delete anything from it.')
            )

        if id not in UserCart.objects.get(user=request.user).recipes.all() \
            .values_list('id', flat=True):
            raise serializers.ValidationError(
                'You do not have such a recipe in your shopping cart.'
            )


def get_recipe_queryset(self: viewsets.ModelViewSet) \
    -> Union[QuerySet, List[Recipe]]:
    """Returns a recipe queryset. It is assumed, that only authorized user
    can use query parameters (filters).
    """
    queryset = Recipe.objects.all()

    if self.request.method in SAFE_METHODS:
        return queryset

    user = User.objects.get(id=self.request.user.id)
    shopping_cart = UserCart.objects.get(user=user) \
        if UserCart.objects.filter(user=user).exists() else None

    is_favorited = self.request.query_params.get('is_favorited')
    is_in_shopping_cart = self.request.query_params.get(
        'is_in_shopping_cart'
    )

    if is_favorited and is_in_shopping_cart:
        return user.favorites.all() + shopping_cart.recipes.all() \
            if shopping_cart else user.favorites.all()

    if is_favorited:
        return user.favorites.all()

    if is_in_shopping_cart:
        return shopping_cart.recipes.all() \
            if shopping_cart else queryset

    return queryset

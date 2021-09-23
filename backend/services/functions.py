from users.models import UserSubscription, UserCart
from recipes.models import Recipe, RecipeIngredient
from users.models import UserCart

from django.http import FileResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.request import Request

from collections import defaultdict


User = get_user_model()


def add_ingredients_to_recipe(recipe: Recipe, validated_data: dict):
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
    """
    if request.user.email == user.email or UserSubscription.objects \
        .filter(author=request.user, follower=user):
        return True
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


def is_favorited(recipe: Recipe, request: Request):
    """Returns True if a particular recipe is user's favorite one,
    otherwise False.
    """
    if recipe in request.user.favorites.all():
        return True
    return False


def is_in_shopping_cart(recipe: Recipe, request: Request):
    """Returns True if specified recipe is in user's shopping cart,
    otherwise False.
    """
    if recipe.id in UserCart.objects.filter(user=request.user) \
        .values_list('recipes', flat=True):
        return True
    return False


def create_subscription(request: Request, id: int) -> User:
    """Creates subscription between two authorized users.
    """
    requested_user = User.objects.get(id=id)
    request.user.subscriptions.add(requested_user)
    return requested_user


def destroy_subscription(request: Request, id: int) -> None:
    """Destroys subscription between two authorized users.
    """
    User.objects.get(id=request.user.id).subscriptions \
        .remove(User.objects.get(id=id))


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


def create_ingredient_dict(request: Request) -> defaultdict:
    """Returns a dict with all ingredients (keys), which were contained
    in the recipes, and their amount (values).
    """
    try:
        ingredient_dict = defaultdict(lambda: 0)
        shopping_cart = request.user.shopping_cart

        recipe_ids = \
            shopping_cart.recipes.all().values_list('id', flat=True)
        _recipe_ingredient = \
            RecipeIngredient.objects.filter(recipe_id__in=recipe_ids)

        for recipe_ingredient in _recipe_ingredient:
            ingredient_dict[recipe_ingredient.ingredient] += \
                recipe_ingredient.amount

        return ingredient_dict
    except (AttributeError, ObjectDoesNotExist) as e:
        raise e


def return_ingredients(request: Request) -> str:
    """Returns a plain txt file, which contains ingredients and their amount.
    """
    try:
        ingredient_dict = create_ingredient_dict(request)

        with open(file=f'temp.txt', mode='w') as file:
            for ingredient in ingredient_dict:
                file.write(
                    (f'{ingredient.name} - '
                     f'{ingredient.measurement_unit} - '
                     f'{ingredient_dict[ingredient]}.')
                )

        return file
    except FileNotFoundError as e:
        raise e

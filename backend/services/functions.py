from users.models import Subscription
from recipies.models import User, Recipe, RecipeIngredient

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
from rest_framework.request import Request

from rest_framework_simplejwt.tokens import RefreshToken

from typing import Union


User = get_user_model()


def create_recipe(validated_data: dict) -> Recipe:
    recipe = Recipe.objects.create(
        author=validated_data['author'],
        name=validated_data['name'],
        image=validated_data['image'],
        text=validated_data['text'],
        cooking_time=validated_data['cooking_time']
    )

    recipe.tags.add(*validated_data['tags'])

    RecipeIngredient.objects.bulk_create([
        RecipeIngredient(
            recipe=recipe,
            ingredient_id=validated_data['ingredients'][position]['id'],
            amount=validated_data['ingredients'][position]['amount']
        ) for position in range(len(validated_data['ingredients']))
    ])

    return recipe


def update_recipe(validated_data: dict) -> Recipe:
    pass


def is_subscribed(user: User, request: Request) -> bool:
    if request.user is user:
        return True

    if Subscription.objects.all() \
        .filter(author=request.user.profile, follower=user.profile):
        return True
    return False


def validate_current_user_password(user: User, password: str) -> str:
    if not check_password(
        password=password,
        encoded=user.password):
        raise serializers.ValidationError('Current password is wrong.')
    return password


def save_new_user_password(user: User, password: str) -> User:
    user.set_password(password)
    user.save()
    return user


def are_proper_credentials(request: Request) -> bool:
    email = request.data.get('email')
    password = request.data.get('password')

    for field in ('email', 'password'):
        if field not in request.data:
            raise serializers.ValidationError(
                f'{field.title()} is a required field.'
            )

    if User.objects.filter(email=email).exists():
        return True
    return False


def get_user(request: Request) -> User:
    return User.objects.get(email=request.data['email'])


def get_access_token():
    return {
        'auth_token': str(RefreshToken.for_user(
                get_user(request=request)
            ).access_token
        ),
    }

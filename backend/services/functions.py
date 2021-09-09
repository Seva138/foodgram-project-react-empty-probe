from recipies.models import Recipe, RecipeIngredient


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

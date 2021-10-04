from recipes.models import (
    Recipe, Ingredient, Tag, RecipeIngredient, RecipeTag
)

from django.contrib import admin
from django.db import transaction
from django.db import IntegrityError


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through

    extra = 1
    max_num = 1


class RecipeTagInline(admin.TabularInline):
    model = Recipe.tags.through

    extra = 1
    max_num = 1


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields=('total_favorites',)
    list_filter = ('tags',)
    inlines = (RecipeIngredientInline, RecipeTagInline)

    @admin.display(empty_value='---empty---')
    def total_favorites(self, obj):
        return obj.userrecipe_set.all().count()


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('slug',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    search_fields = ('recipe__name',)


class RecipeTagAdmin(admin.ModelAdmin):
    search_fields = ('recipe__name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)

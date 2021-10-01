from recipes.models import Recipe, Ingredient, Tag

from django.contrib import admin


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    readonly_fields=('total_favorites',)
    list_filter = ('tags',)

    @admin.display(empty_value='---empty---')
    def total_favorites(self, obj):
        return obj.userrecipe_set.all().count()


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('slug',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)

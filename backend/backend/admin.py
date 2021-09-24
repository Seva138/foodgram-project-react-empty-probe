from users.models import User
from recipes.models import Recipe, Ingredient, Tag

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')


class RecipeAdmin(admin.ModelAdmin):
    fields = ('author', 'name', 'total_favorites')
    readonly_fields=('total_favorites',)
    list_filter = ('author', 'name', 'tags')

    @admin.display(empty_value='---empty---')
    def total_favorites(self, obj):
        return obj.userrecipe_set.all().count()


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_filter = ('name',)


empty_value_display = '---empty---'
admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)

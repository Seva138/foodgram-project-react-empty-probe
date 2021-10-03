from users.models import User, UserCart, UserSubscription, UserRecipe

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_filter = ('email', 'username')


class UserCartAdmin(admin.ModelAdmin):
    search_fields = ('user__email',)


class UserSubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('author__email',)


class UserRecipeAdmin(admin.ModelAdmin):
    search_fields = ('user__email',)


admin.site.empty_value_display = '---empty---'
admin.site.register(User, UserAdmin)
admin.site.register(UserCart, UserCartAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
admin.site.register(UserRecipe, UserRecipeAdmin)

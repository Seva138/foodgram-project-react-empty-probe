from users.models import User, UserCart

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    search_fields = ('email',)
    list_filter = ('email', 'username')
    verbose_name = 'Пользователь'


class UserCartAdmin(admin.ModelAdmin):
    search_fields = ('user__email',)


admin.site.empty_value_display = '---empty---'
admin.site.register(User, UserAdmin)
admin.site.register(UserCart, UserCartAdmin)

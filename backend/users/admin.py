from users.models import User

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')


admin.site.empty_value_display = '---empty---'
admin.site.register(User, UserAdmin)

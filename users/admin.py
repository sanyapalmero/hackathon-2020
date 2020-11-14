from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin

from .models import User


admin.site.unregister(auth.models.Group)


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "last_login", "created_at")
    search_fields = ("email", "username", "role")
    readonly_fields = ("last_login",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)

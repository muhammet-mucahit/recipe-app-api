from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core import models

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name']
    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'password')
            }
        ),
        (
            _('Personal Info'),
            {
                'fields': ('first_name', 'last_name')
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important Dates'),
            {
                'fields': ('date_joined', 'last_login')
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = (
        'id',
        'email',
        'name',
        'surname',
        'phone',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
    )
    search_fields = (
        'email',
        'name',
        'surname',
        'phone',
    )
    filter_horizontal = (
        'groups',
        'user_permissions',
        'favorites',
    )

    fieldsets = (
        (
            'Данные для входа',
            {
                'fields': (
                    'email',
                    'password',
                ),
            },
        ),
        (
            'Личная информация',
            {
                'fields': (
                    'name',
                    'surname',
                    'avatar',
                    'phone',
                    'github_url',
                    'about',
                    'favorites',
                ),
            },
        ),
        (
            'Права доступа',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'Важные даты',
            {
                'fields': (
                    'last_login',
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            'Создание пользователя',
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'name',
                    'surname',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )

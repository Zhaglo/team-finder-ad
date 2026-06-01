from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'status',
        'created_at',
        'participants_count',
    )
    list_filter = (
        'status',
        'created_at',
    )
    search_fields = (
        'name',
        'description',
        'owner__email',
        'owner__name',
        'owner_surname',
    )
    readonly_fields = (
        'created_at',
    )
    filter_horizontal = (
        'participants',
    )

    @admin.display(description='Участников')
    def participants_count(self, obj):
        return obj.participants.count()

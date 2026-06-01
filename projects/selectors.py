from .models import Project


def get_projects_with_related():
    return Project.objects.select_related('owner').prefetch_related('participants')


def get_projects_list():
    return get_projects_with_related().order_by('-created_at')


def get_favorite_projects_for_user(user):
    return (
        user.favorites
        .select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )

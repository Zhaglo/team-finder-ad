from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from team_finder.constants import PROJECTS_PER_PAGE
from team_finder.pagination import paginate_queryset

from .forms import ProjectForm
from .models import Project
from .selectors import (
    get_favorite_projects_for_user,
    get_projects_list,
    get_projects_with_related,
)


def project_list(request):
    projects = get_projects_list()

    page_obj, query_prefix = paginate_queryset(
        request,
        projects,
        PROJECTS_PER_PAGE,
    )

    return render(
        request,
        'projects/project_list.html',
        {
            'projects': projects,
            'page_obj': page_obj,
            'query_prefix': query_prefix,
        }
    )


def project_detail(request, project_id):
    project = get_object_or_404(
        get_projects_with_related(),
        id=project_id
    )

    return render(
        request,
        'projects/project-details.html',
        {
            'project': project,
        }
    )


@login_required
def favorite_projects(request):
    projects = get_favorite_projects_for_user(request.user)

    return render(
        request,
        'projects/favorite_projects.html',
        {
            'projects': projects,
        }
    )


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)

        return redirect('projects:project_detail', project_id=project.id)

    return render(
        request,
        'projects/create-project.html',
        {
            'form': form,
            'is_edit': False,
        }
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden('Редактировать проект может только автор!')

    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid():
        form.save()
        return redirect('projects:project_detail', project_id=project.id)

    return render(
        request,
        'projects/create-project.html',
        {
            'form': form,
            'is_edit': True,
        }
    )


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return JsonResponse(
            {
                'status': 'error',
                'detail': 'forbidden'
            },
            status=HTTPStatus.FORBIDDEN,
        )

    if project.status != Project.Status.OPEN:
        return JsonResponse(
            {
                'status': 'error',
                'detail': 'project is already closed'
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    project.status = Project.Status.CLOSED
    project.save(update_fields=('status',))

    return JsonResponse(
        {
            'status': 'ok',
            'project_status': Project.Status.CLOSED,
        }
    )


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner == request.user:
        return JsonResponse(
            {
                'status': 'error',
                'detail': 'owner cannot toggle participation',
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    participant = project.participants.filter(id=request.user.id).exists()

    if participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse(
        {
            'status': 'ok',
            'participant': not participant,
        }
    )


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    favorited = request.user.favorites.filter(id=project.id).exists()

    if favorited:
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)

    return JsonResponse(
        {
            'status': 'ok',
            'favorited': not favorited,
        }
    )

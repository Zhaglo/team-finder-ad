from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse

from .models import Project
from .forms import ProjectForm


PROJECTS_PER_PAGE = 12


def project_list(request):
    projects = (
        Project.objects
        .select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )

    paginator = Paginator(projects, PROJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'projects/project_list.html',
        {
            'projects': projects,
            'page_obj': page_obj,
            'query_prefix': '',
        }
    )

def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects
        .select_related('owner')
        .prefetch_related('participants'),
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
    projects = (
        request.user.favorites
        .select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )

    return render(
        request,
        'projects/favorite_projects.html',
        {
            'projects': projects,
        }
    )

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)

            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm()

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

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', project_id=project.id)

    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        'projects/create-project.html',
        {
            'form': form,
            'is_edit': True,
        }
    )

@login_required
def complete_project(request, project_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return JsonResponse({'status': 'error', 'detail': 'forbidden'}, status=403)

    if project.status != Project.Status.OPEN:
        return JsonResponse(
            {
                'status': 'error',
                'detail': 'project is already closed'
            },
            status=400
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
def toggle_participate(request, project_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    project = get_object_or_404(Project, id=project_id)

    if project.owner == request.user:
        return JsonResponse(
            {
                'status': 'error',
                'detail': 'owner cannot toggle participation',
            },
            status=400,
        )

    if request.user in project.participants.all():
        project.participants.remove(request.user)
        participant = False
    else:
        project.participants.add(request.user)
        participant = True

    return JsonResponse(
        {
            'status': 'ok',
            'participant': participant,
        }
    )

@login_required
def toggle_favorite(request, project_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    project = get_object_or_404(Project, id=project_id)

    if request.user.favorites.filter(id=project.id).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True

    return JsonResponse(
        {
            'status': 'ok',
            'favorited': favorited,
        }
    )

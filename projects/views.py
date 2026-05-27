from django.shortcuts import render
from django.http import HttpResponse


def project_list(request):
    return HttpResponse('Project list')


def favorite_projects(request):
    return HttpResponse('Favorite projects')


def create_project(request):
    return HttpResponse('Create project')


def project_detail(request, project_id):
    return HttpResponse(f'Project detail: {project_id}')


def edit_project(request, project_id):
    return HttpResponse(f'Edit project: {project_id}')


def complete_project(request, project_id):
    return HttpResponse(f'Complete project: {project_id}')


def toggle_participate(request, project_id):
    return HttpResponse(f'Toggle participate: {project_id}')


def toggle_favorite(request, project_id):
    return HttpResponse(f'Toggle favorite: {project_id}')

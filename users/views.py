from django.shortcuts import render
from django.http import HttpResponse


def register(request):
    return HttpResponse('Register')


def login_view(request):
    return HttpResponse('Login')


def logout_view(request):
    return HttpResponse('Logout')


def user_list(request):
    return HttpResponse('User list')


def user_detail(request, user_id):
    return HttpResponse(f'User detail: {user_id}')


def edit_profile(request):
    return HttpResponse('Edit profile')


def change_password(request):
    return HttpResponse('Change password')

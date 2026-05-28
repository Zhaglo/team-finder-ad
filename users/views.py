from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    CustomPasswordChangeForm,
    LoginForm,
    ProfileEditForm,
    RegisterForm,
)


User = get_user_model()

USERS_PER_PAGE = 12


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegisterForm()

    return render(
        request,
        'users/register.html',
        {
            'form': form,
        }
    )

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('projects:project_list')
    else:
        form = LoginForm(request)

    return render(
        request,
        'users/login.html',
        {
            'form': form,
        }
    )

def logout_view(request):
    logout(request)
    return redirect('projects:project_list')

def user_list(request):
    active_filter = request.GET.get('filter')

    users = User.objects.all().order_by('-id')

    if request.user.is_authenticated and active_filter:
        current_user = request.user

        if active_filter == 'owners-of-favorite-projects':
            users = User.objects.filter(
                owned_projects__in=current_user.favorites.all()
            )
        elif active_filter == 'owners-of-participating-projects':
            users = User.objects.filter(
                owned_projects__in=current_user.participated_projects.all()
            )
        elif active_filter == 'interested-in-my-projects':
            users = User.objects.filter(
                favorites__in=current_user.owned_projects.all()
            )
        elif active_filter == 'participants-of-my-projects':
            users = User.objects.filter(
                participated_projects__in=current_user.owned_projects.all()
            )

        users = users.exclude(id=current_user.id).distinct().order_by('-id')

    paginator = Paginator(users, USERS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_prefix = ''
    if active_filter:
        query_prefix = f'filter={active_filter}&'

    return render(
        request,
        'users/participants.html',
        {
            'participants': users,
            'page_obj': page_obj,
            'active_filter': active_filter,
            'query_prefix': query_prefix,
        }
    )

def user_detail(request, user_id):
    user = get_object_or_404(
        User.objects.prefetch_related('owned_projects__participants'),
        id=user_id,
    )

    return render(
        request,
        'users/user-details.html',
        {
            'user': user,
        }
    )

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():
            form.save()
            return redirect('users:user_detail', user_id=request.user.id)
    else:
        form = ProfileEditForm(instance=request.user)

    return render(
        request,
        'users/edit_profile.html',
        {
            'form': form,
            'user': request.user,
        }
    )

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:user_detail', user_id=request.user.id)
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(
        request,
        'users/change_password.html',
        {
            'form': form,
        }
    )

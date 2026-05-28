from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from projects.models import Project
from .managers import UserManager
from .avatar import generate_user_avatar


def user_avatar_upload_path(instance, filename):
    return f'users/avatars/{filename}'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        blank=False,
        unique=True,
        verbose_name='Email'
    )
    name = models.CharField(
        max_length=124,
        blank=False,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=124,
        blank=False,
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(
        upload_to=user_avatar_upload_path,
        blank=False,
        verbose_name='Аватар'
    )
    phone = models.CharField(
        max_length=12,
        blank=False,
        verbose_name='Телефон'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='GitHub'
    )
    about = models.TextField(
        max_length=256,
        blank=True,
        verbose_name='Описание профиля'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )
    favorites = models.ManyToManyField(
        Project,
        blank=True,
        related_name='interested_users',
        verbose_name='Избранное'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    def save(self, *args, **kwargs):
        if not self.avatar:
            filename, avatar_file = generate_user_avatar(self.name)
            self.avatar.save(filename, avatar_file, save=False)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'

    @property
    def full_name(self):
        return f'{self.name} {self.surname}'

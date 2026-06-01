from django.conf import settings
from django.db import models
from django.urls import reverse

from team_finder.constants import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_MAX_LENGTH,
)


class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Открыт'
        CLOSED = 'closed', 'Закрыт'

    name = models.CharField(
        max_length=PROJECT_NAME_MAX_LENGTH,
        verbose_name='Название проекта'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание проекта'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Автор проекта'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания проекта'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='Ссылка на GitHub'
    )
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name='Статус проекта'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники проекта'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'project_id': self.id})

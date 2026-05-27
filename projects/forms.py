from django import forms
from django.core.exceptions import ValidationError

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        labels = {
            'name': 'Название проекта',
            'description': 'Описание проекта',
            'github_url': 'Ссылка на GitHub',
            'status': 'Статус',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название проекта'}),
            'description': forms.Textarea(attrs={'placeholder': 'Опишите проект'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
        }

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')

        if github_url and 'github.com' not in github_url.lower():
            raise ValidationError('Ссылка должна вести на GitHub')

        return github_url

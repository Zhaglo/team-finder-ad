from django import forms

from team_finder.form_mixins import GithubUrlValidatorMixin

from .models import Project


class ProjectForm(GithubUrlValidatorMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название проекта'}),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Опишите проект',
                    'rows': 4,
                }
            ),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
        }

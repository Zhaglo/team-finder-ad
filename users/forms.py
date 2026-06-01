import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from team_finder.form_mixins import GithubUrlValidatorMixin

from .models import User
from .services import normalize_phone


PHONE_PATTERN = re.compile(r'^(\+7|8)\d{10}$')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user = authenticate(
                self.request,
                username=email,
                password=password,
            )

            if self.user is None:
                raise ValidationError('Неверный email или пароль.')

            if not self.user.is_active:
                raise ValidationError('Пользователь заблокирован.')

        return cleaned_data

    def get_user(self):
        return self.user


class ProfileEditForm(GithubUrlValidatorMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'avatar', 'about', 'phone', 'github_url')
        widgets = {
            'avatar': forms.FileInput(
                attrs={
                    'class': 'hidden-avatar-input',
                    'accept': 'image/*',
                }
            ),
            'about': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            return phone

        phone = phone.strip()

        if not PHONE_PATTERN.match(phone):
            raise ValidationError('Введите номер в формате 8XXXXXXXXXX или +7XXXXXXXXXX.')

        normalized_phone = normalize_phone(phone)

        users_with_same_phone = User.objects.filter(phone=normalized_phone)

        if self.instance.pk:
            users_with_same_phone = users_with_same_phone.exclude(pk=self.instance.pk)

        if users_with_same_phone.exists():
            raise ValidationError('Пользователь с таким номером телефона уже существует.')

        return normalized_phone


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput,
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput,
    )

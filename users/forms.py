from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'avatar', 'phone', 'country')
        labels = {
            'email': 'Электронная почта',
            'username': 'Имя пользователя',
            'avatar': 'Аватар',
            'phone': 'Телефон',
            'country': 'Страна',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm):
    """Форма входа по email и паролю."""

    username = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    )

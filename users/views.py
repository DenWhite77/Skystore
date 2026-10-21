from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserLoginForm, UserProfileForm, UserRegisterForm


class RegisterView(CreateView):
    """Регистрация нового пользователя."""

    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        send_mail(
            subject='Добро пожаловать в Skystore!',
            message=(
                f'Здравствуйте, {user.username}!\n\n'
                f'Спасибо за регистрацию на Skystore.\n'
                f'Ваш аккаунт: {user.email}\n\n'
                f'Команда Skystore'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return response


class UserLoginView(LoginView):
    """Вход по email и паролю."""

    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Выход из системы."""

    next_page = reverse_lazy('users:login')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля текущего пользователя."""

    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

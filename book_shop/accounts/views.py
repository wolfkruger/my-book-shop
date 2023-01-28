from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import *


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    """def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('login')"""


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # установить срок действия сеанса на 0 секунд.
            # Таким образом, он автоматически закроет сеанс после закрытия браузера.
            self.request.session.set_expiry(0)

            # Установите сеанс как измененный, чтобы принудительно сохранить обновления данных/файлы cookie.
            self.request.session.modified = True

            # в противном случае сеанс браузера будет длиться столько же, сколько время файла cookie сеанса
            # «SESSION_COOKIE_AGE», определенное в settings.py.
        return super(LoginUser, self).form_valid(form)


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return render(request, 'accounts/logout.html')


@login_required
def user_profile(request):
    return render(request, 'accounts/user_profile.html')


class ChangeUserData(UpdateView):
    form_class = ChangeUserDataForm
    template_name = 'accounts/change_user_data.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class ChangeUserPassword(PasswordChangeView):
    form_class = ChangeUserPasswordForm
    template_name = 'accounts/change_user_password.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserResetPassword(PasswordResetView):
    model = User
    template_name = 'accounts/user_password_reset.html'


class UserResetPasswordDone(PasswordResetDoneView):
    model = User
    template_name = 'accounts/user_password_reset_sent.html'


class UserResetPasswordConfirm(PasswordResetConfirmView):
    model = User
    template_name = 'accounts/user_password_confirm.html'


class UserResetPasswordComplete(PasswordResetCompleteView):
    model = User
    template_name = 'accounts/user_password_complete.html'

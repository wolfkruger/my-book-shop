from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.contrib.auth.forms import User
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form_input',
                                                             'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form_input',
                                                                 'placeholder': 'Пароль'}))
    remember_me = forms.BooleanField(required=False, label='Запомнить меня')

    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь не найден")
        return username


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                                       'placeholder': 'Имя пользователя'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                            'placeholder': 'Имя'}), required=False)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                               'placeholder': 'Фамилия'}),
                                required=False)
    email = forms.EmailField(label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={'class': 'form_input', 'placeholder': 'Электронная почта'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input',
                                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'class': 'form_input', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ChangeUserDataForm(UserChangeForm):
    username = forms.CharField(label='Имя пользователя:', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                                        'placeholder': 'username'}))
    first_name = forms.CharField(label='Имя:', required=False, widget=forms.TextInput(attrs={'class': 'form_input',
                                                                                             'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия:', required=False, widget=forms.TextInput(attrs={'class': 'form_input',
                                                                                                'placeholder': 'Фамилия'}))
    email = forms.CharField(label='Электронная почта:', widget=forms.EmailInput(attrs={'class': 'form_input',
                                                                                       'placeholder': 'Электронная почта'}))
    password = forms.CharField(label='', widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class ChangeUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'

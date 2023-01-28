from django import forms
from django.contrib.auth.forms import UserChangeForm

from my_books.models import *
from django.contrib.auth.models import User


class AddBook(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'


class UserInfoForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'groups', 'user_permissions', 'is_active',
                  'is_staff', 'is_superuser', 'last_login', 'date_joined',)
        widgets = {'groups': forms.CheckboxSelectMultiple, 'user_permissions': forms.CheckboxSelectMultiple}


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class AddGenreForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = '__all__'

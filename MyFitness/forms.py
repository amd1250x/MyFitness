from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class UserForm(ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


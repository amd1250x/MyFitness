from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from MyFitness.models import FitnessLog


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


class FitnessLogForm(ModelForm):

    activity_types = ((1, 'Weighted Lifting'), (2, 'Body weight Lifting'), (3, 'Cardiovascular'))
    unit_types = ((1, 'Pounds'), (2, 'Kilograms'))

    user = forms.CharField(label='Username', max_length=200)
    ename = forms.CharField(label='Name', max_length=200)
    date = forms.DateField(label='Date')
    activity = forms.ChoiceField(label='Exercise', choices=activity_types)
    reps = forms.IntegerField(label='Repetitions/Time')
    weight = forms.IntegerField(label='Weight')
    units = forms.ChoiceField(label='Units', choices=unit_types)

    class Meta:
        model = FitnessLog
        fields = ('user',
                  'ename',
                  'date',
                  'activity',
                  'reps',
                  'weight',
                  'units')

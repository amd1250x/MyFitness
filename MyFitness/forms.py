from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from MyFitness.models import FitnessLog, BodyWeightLog
import datetime


class UserForm(ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(ModelForm):
    username = forms.CharField(label='Username',
                               max_length=100,
                               widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class FitnessLogForm(ModelForm):

    activity_types = ((1, 'Weighted Lifting'), (2, 'Body weight Lifting'), (3, 'Cardiovascular'))
    w_unit_types = ((1, 'Pounds'), (2, 'Kilograms'))
    r_unit_types = ((1, 'Seconds'), (2, 'Minutes'), (3, 'Repetitions'))
    today = datetime.datetime.today()

    ename = forms.CharField(label='Name', max_length=200)
    date = forms.DateField(label='Date', initial=datetime.datetime.today().strftime("%m/%d/%Y"),
                           widget=forms.TextInput(attrs={'id': 'datepicker'}))
    activity = forms.ChoiceField(label='Exercise', choices=activity_types, widget=forms.RadioSelect())
    reps = forms.IntegerField(label='Repetitions/Time')
    r_units = forms.ChoiceField(label='Units', choices=r_unit_types, widget=forms.RadioSelect())
    sets = forms.IntegerField(label='Sets')
    weight = forms.IntegerField(label='Weight')
    w_units = forms.ChoiceField(label='Units', choices=w_unit_types, widget=forms.RadioSelect())

    class Meta:
        model = FitnessLog
        fields = ('ename',
                  'date',
                  'activity',
                  'reps',
                  'r_units',
                  'sets',
                  'weight',
                  'w_units')


class DelLogForm(ModelForm):

    class Meta:
        model = FitnessLog
        fields = ()

class BodyWeightLogForm(ModelForm):

    time_of_day = ((1, 'Morning'), (2, 'Afternoon'))
    w_unit_types = ((1, 'Pounds'), (2, 'Kilograms'))

    weight = forms.FloatField(label='Weight', initial=150)
    w_units = forms.ChoiceField(label='Units', choices=w_unit_types, widget=forms.RadioSelect())
    date = forms.DateField(label='Date', initial=datetime.datetime.today().strftime("%m/%d/%Y"),
                                         widget=forms.TextInput(attrs={'id': 'datepicker'}))
    # time of day
    tod = forms.ChoiceField(label='Time of Day', choices=time_of_day,
                                                 widget=forms.RadioSelect())

    class Meta:
        model = BodyWeightLog
        fields = ('weight',
                  'w_units',
                  'date',
                  'tod')

class DelBodyWeightLogForm(ModelForm):

    class Meta:
        model = BodyWeightLog
        fields = ()

from django.contrib.auth.models import User
from django.forms import ModelForm, ModelMultipleChoiceField
from django import forms
from MyFitness.models import FitnessLog, BodyWeightLog, WorkoutExercise, WorkoutLog, Workout
import datetime

activity_types = ((1, 'Weighted Lifting'), (2, 'Body weight Lifting'), (3, 'Cardiovascular'))
w_unit_types = ((1, 'Pounds'), (2, 'Kilograms'))
r_unit_types = ((1, 'Seconds'), (2, 'Minutes'), (3, 'Repetitions'))
today = datetime.datetime.today()


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

    def __init__(self, *args, **kwargs):
        # Get the user field from our args
        user = kwargs.pop('user')
        # sorted(set(...)) removes duplicates in the list
        exercises = sorted(set(((str(e), str(e)) for e in FitnessLog.objects.all().filter(owner=user))))
        super(FitnessLogForm, self).__init__(*args, **kwargs)
        self.fields['ename'] = forms.ChoiceField(choices=exercises)
        self.fields['ename'].required = False

    ename_str = forms.CharField(label='Name', max_length=100, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'New Exercise'}))
    date = forms.DateField(label='Date', initial=datetime.datetime.today().strftime("%m/%d/%Y"),
                           widget=forms.TextInput(attrs={'id': 'datepicker'}))
    activity = forms.ChoiceField(label='Exercise', choices=activity_types, widget=forms.RadioSelect())
    reps = forms.IntegerField(label='Repetitions/Time')
    r_units = forms.ChoiceField(label='Units', choices=r_unit_types, widget=forms.RadioSelect())
    sets = forms.IntegerField(label='Sets')
    weight = forms.IntegerField(label='Weight', required=False)
    w_units = forms.ChoiceField(label='Units', choices=w_unit_types, widget=forms.RadioSelect())

    class Meta:
        model = FitnessLog
        fields = ('ename',
                  'ename_str',
                  'date',
                  'activity',
                  'reps',
                  'r_units',
                  'sets',
                  'weight',
                  'w_units',
                  )


class EditLogForm(ModelForm):

    ename_str = forms.CharField(label='Name', max_length=100, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'New Exercise'}))

    class Meta:
        model = FitnessLog
        fields = ('ename',
                  'ename_str',
                  'date',
                  'activity',
                  'reps',
                  'r_units',
                  'sets',
                  'weight',
                  'w_units',
                  )


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


class WorkoutForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        self.fields['color'] = forms.CharField(label='Color', max_length=6)
        self.fields['color'].widget = forms.TextInput(attrs={'class': 'jscolor'})

    name = forms.CharField(label='Name', max_length=100)
    desc = forms.CharField(label='Description', max_length=100)

    class Meta:
        model = Workout
        fields = ('name',
                  'desc',
                  'color')


class EditWorkoutForm(ModelForm):

    class Meta:
        model = Workout
        fields = ('name',
                  'desc',
                  'color')


class WorkoutExerciseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # Get the user field from our args
        user = kwargs.pop('user')
        # sorted(set(...)) removes duplicates in the list
        workouts = sorted(set(((str(e), str(e)) for e in Workout.objects.all().filter(owner=user))))
        super(WorkoutExerciseForm, self).__init__(*args, **kwargs)
        self.fields['workout'] = forms.ChoiceField(choices=workouts)
        self.fields['workout'].required = False

    ename = forms.CharField(label='Exercise Name', max_length=100)
    activity = forms.ChoiceField(label='Exercise', choices=activity_types, widget=forms.RadioSelect())
    reps = forms.IntegerField(label='Repetitions/Time')
    r_units = forms.ChoiceField(label='Units', choices=r_unit_types, widget=forms.RadioSelect())
    sets = forms.IntegerField(label='Sets')

    class Meta:
        model = WorkoutExercise
        fields = ('ename',
                  'workout',
                  'activity',
                  'reps',
                  'r_units',
                  'sets')


class EditWorkoutExerciseForm(ModelForm):

    class Meta:
        model = WorkoutExercise
        fields = ('ename',
                  'workout',
                  'activity',
                  'reps',
                  'r_units',
                  'sets')


class WorkoutLogForm(ModelForm):

    def __init__(self, *args, **kwargs):
        # Get the user field from our args
        user = kwargs.pop('user')
        workout_id = kwargs.pop('workout_id')
        my_workout = Workout.objects.get(id=workout_id)
        select_workouts = WorkoutExercise.objects.all().filter(workout=my_workout)
        super(WorkoutLogForm, self).__init__(*args, **kwargs)
        self.fields['workout'] = forms.CharField(max_length=100)
        self.fields['workout'].widget = forms.TextInput(attrs={'type': 'hidden'})
        self.fields['workout'].required = False
        self.fields['weights'] = forms.CharField(label='Weights', max_length=200)
        init_str = ""
        for w in select_workouts:
            init_str += w.ename + ", "
        self.fields['weights'].widget = forms.TextInput(attrs={'placeholder': init_str,
                                                               'size': len(init_str)})

    date = forms.DateField(label='Date', initial=datetime.datetime.today().strftime("%m/%d/%Y"),
                           widget=forms.TextInput(attrs={'id': 'datepicker'}))
    w_units = forms.ChoiceField(label='Units', choices=w_unit_types, widget=forms.RadioSelect())

    class Meta:
        model = WorkoutLog
        fields = ('date',
                  'workout',
                  'weights',
                  'w_units')


class EditWorkoutLogForm(ModelForm):

    class Meta:
        model = WorkoutLog
        fields = ('date',
                  'workout',
                  'weights',
                  'w_units')


class DelWorkoutLogForm(ModelForm):

    class Meta:
        model = WorkoutLog
        fields = ()


class DelWorkoutExerciseForm(ModelForm):

    class Meta:
        model = WorkoutLog
        fields = ()
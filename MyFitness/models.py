from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
activity_types = ((1, 'Weighted Lifting'), (2, 'Body weight Lifting'), (3, 'Cardiovascular'))
w_unit_types = ((1, 'Pounds'), (2, 'Kilograms'))
w_contract = ['lbs.', 'kg.']
r_unit_types = ((1, 'Seconds'), (2, 'Minutes'), (3, 'Repetitions'))
r_contract = ['sec.', 'min.', 'reps']
time_of_day = ((1, 'Morning'), (2, 'Afternoon'))


class Workout(models.Model):
    id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Name', max_length=100)
    desc = models.CharField('Description', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='workouts', on_delete=models.CASCADE)
    count = models.IntegerField('Number of Exercises')
    color = models.CharField('Color', max_length=6)

    def __str__(self):
        return self.name


class FitnessLog(models.Model):
    id = models.AutoField('ID', primary_key=True)
    ename = models.CharField('Name', max_length=100)
    ename_str = models.CharField('Str Name', max_length=100)
    date = models.DateField('Date')
    activity = models.IntegerField('Exercise', choices=activity_types)
    reps = models.IntegerField('Repetitions/Time')
    r_units = models.IntegerField('Units', choices=r_unit_types)
    sets = models.IntegerField('Sets')
    weight = models.IntegerField('Weight', default=0)
    w_units = models.IntegerField('Units', choices=w_unit_types)
    workout = models.ForeignKey('Workout', related_name='workout', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='fitness_logs', on_delete=models.CASCADE)

    def __str__(self):
        return self.ename

    def get_weight_unit(self):
        return w_contract[self.w_units-1]

    def get_reps_unit(self):
        return r_contract[self.r_units-1]


class BodyWeightLog(models.Model):
    id = models.AutoField('ID', primary_key=True)
    weight = models.FloatField('Weight', default=150)
    w_units = models.IntegerField('Units', choices=w_unit_types)
    date = models.DateField('Date')
    # time of day
    tod = models.IntegerField('Time of Day', choices=time_of_day)
    owner = models.ForeignKey('auth.User', related_name='bodyweight_logs', on_delete=models.CASCADE)

    def __str__(self):
        return self.owner + '-' + str(self.date) + '-' + str(time_of_day[self.tod-1][1])

    def get_weight_unit(self):
        return w_contract[self.w_units-1]


class WorkoutExercise(models.Model):
    id = models.AutoField('ID', primary_key=True)
    ename = models.CharField('Str Name', max_length=100)
    workout = models.CharField('Workout', max_length=100)
    activity = models.IntegerField('Exercise', choices=activity_types)
    reps = models.IntegerField('Repetitions/Time')
    r_units = models.IntegerField('Units', choices=r_unit_types)
    sets = models.IntegerField('Sets')
    owner = models.ForeignKey('auth.User', related_name='workout_exercises', on_delete=models.CASCADE)

    def __str__(self):
        return self.workout


class WorkoutLog(models.Model):
    id = models.AutoField('ID', primary_key=True)
    date = models.DateField('Date')
    workout = models.CharField('Workout', max_length=100)
    weights = models.CharField('Weights', max_length=200)
    w_units = models.IntegerField('Units', choices=w_unit_types)
    owner = models.ForeignKey('auth.User', related_name='workout_exercise_logs', on_delete=models.CASCADE)

    def __str__(self):
        return self.workout

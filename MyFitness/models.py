from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
activity_types = ((1, 'Weighted Lifting'), (2, 'Body weight Lifting'), (3, 'Cardiovascular'))
w_unit_types = ((1, 'Pounds'), (2, 'Kilograms'))
w_contract = ['lbs.', 'kg']
r_unit_types = ((1, 'Seconds'), (2, 'Minutes'), (3, 'Repetitions'))
r_contract = ['sec.', 'min.', 'reps']
time_of_day = ((1, 'Morning'), (2, 'Afternoon'))
list_of_days = ((1, 'Monday'),
                (2, 'Tuesday'),
                (3, 'Wednesday'),
                (4, 'Thursday'),
                (5, 'Friday'),
                (6, 'Saturday'),
                (7, 'Sunday'))


class FitnessLog(models.Model):
    id = models.AutoField('ID', primary_key=True)
    user = models.CharField('Username', max_length=100)
    ename = models.CharField('Name', max_length=100)
    date = models.DateField('Date')
    activity = models.IntegerField('Exercise', choices=activity_types)
    reps = models.IntegerField('Repetitions/Time')
    r_units = models.IntegerField('Units', choices=r_unit_types)
    sets = models.IntegerField('Sets')
    weight = models.IntegerField('Weight', default=0)
    w_units = models.IntegerField('Units', choices=w_unit_types)

    def __str__(self):
        return self.ename

    def get_weight_unit(self):
        return w_contract[self.w_units-1]

    def get_reps_unit(self):
        return r_contract[self.r_units-1]

class BodyWeightLog(models.Model):
    id = models.AutoField('ID', primary_key=True)
    user = models.CharField('Username', max_length=100)
    weight = models.FloatField('Weight', default=150)
    w_units = models.IntegerField('Units', choices=w_unit_types)
    date = models.DateField('Date')
    # time of day
    tod = models.IntegerField('Time of Day', choices=time_of_day)

    def __str__(self):
        return self.user + '-' + str(self.date) + '-' + str(time_of_day[self.tod-1][1])

    def get_weight_unit(self):
        return w_contract[self.w_units-1]

class WorkoutDay(models.Model):
    id = models.AutoField('ID', primary_key=True)
    user = models.CharField('Username', max_length=100)
    day = models.IntegerField('Day', choices=list_of_days)

    def __str__(self):
        return self.user + '-' + str(list_of_days[self.day-1][1])

    def get_expanded(self):
        return str(list_of_days[self.day-1][1])
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
activity_types = ((1, 'Weighted Lifting'), (2, 'Body weight Lifting'), (3, 'Cardiovascular'))
w_unit_types = ((1, 'Pounds'), (2, 'Kilograms'))
r_unit_types = ((1, 'Seconds'), (2, 'Minutes'), (3, 'Repetitions'))

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



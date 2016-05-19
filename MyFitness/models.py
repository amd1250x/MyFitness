from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
activity_types = ((1, 'Weighted Lifting'), (2, 'Body weight Lifting'), (3, 'Cardiovascular'))
unit_types = ((1, 'Pounds'), (2, 'Kilograms'))


class FitnessLog(models.Model):
    id = models.AutoField('ID', primary_key=True)
    user = models.CharField('Username', max_length=100)
    ename = models.CharField('Name', max_length=100)
    date = models.DateField('Date')
    activity = models.IntegerField('Exercise', choices=activity_types)
    reps = models.IntegerField('Repetitions/Time')
    weight = models.IntegerField('Weight', default=0)
    units = models.IntegerField('Units', choices=unit_types)

    def __str__(self):
        return self.ename



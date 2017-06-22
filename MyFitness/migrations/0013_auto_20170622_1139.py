# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-22 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyFitness', '0012_fitnesslog_workout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnesslog',
            name='wlog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workout_log', to='MyFitness.WorkoutLog'),
        ),
        migrations.AlterField(
            model_name='fitnesslog',
            name='workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workout', to='MyFitness.Workout'),
        ),
    ]

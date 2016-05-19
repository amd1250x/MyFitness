# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-19 04:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyFitness', '0003_fitnesslog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnesslog',
            name='id',
        ),
        migrations.AddField(
            model_name='fitnesslog',
            name='weight',
            field=models.IntegerField(default=1, verbose_name='Weight'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fitnesslog',
            name='date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='fitnesslog',
            name='ename',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='fitnesslog',
            name='reps',
            field=models.IntegerField(verbose_name='Repetitions/Time'),
        ),
        migrations.AlterField(
            model_name='fitnesslog',
            name='units',
            field=models.IntegerField(choices=[(1, 'Pounds'), (2, 'Kilograms')], verbose_name='Units'),
        ),
        migrations.AlterField(
            model_name='fitnesslog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]

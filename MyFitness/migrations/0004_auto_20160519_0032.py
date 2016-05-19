# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-19 05:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyFitness', '0003_fitnesslog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnesslog',
            name='user',
        ),
        migrations.AddField(
            model_name='fitnesslog',
            name='username',
            field=models.CharField(default=1, max_length=200, verbose_name='Username'),
            preserve_default=False,
        ),
    ]

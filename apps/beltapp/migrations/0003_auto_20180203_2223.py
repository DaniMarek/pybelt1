# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-03 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beltapp', '0002_quote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='favorite',
            field=models.ManyToManyField(related_name='faves', to='beltapp.User'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='beltapp.User'),
        ),
    ]
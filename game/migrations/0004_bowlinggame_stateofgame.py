# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_bowlinggame_strikespareinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='bowlinggame',
            name='StateOfGame',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-19 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('captioning', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagecaptioning',
            name='caption',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]
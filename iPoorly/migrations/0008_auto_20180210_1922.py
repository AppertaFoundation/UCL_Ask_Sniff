# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-02-10 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iPoorly', '0007_auto_20180210_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diarylog',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-01-02 20:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iPoorly', '0003_auto_20180101_2225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['categoryName']},
        ),
        migrations.AlterModelOptions(
            name='child',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='diarylog',
            options={'ordering': ['diary_id']},
        ),
        migrations.AlterModelOptions(
            name='heading',
            options={'ordering': ['headingId']},
        ),
        migrations.AlterModelOptions(
            name='subheading',
            options={'ordering': ['subHeadingId']},
        ),
    ]

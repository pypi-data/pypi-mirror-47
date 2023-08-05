# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-22 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waldur_jira', '0011_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='backend_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='backend_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='backend_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

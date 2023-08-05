# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-13 07:10
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_offering_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offering',
            name='attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=''),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-26 09:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0034_bootstrap_statuses'),
    ]

    operations = [
        migrations.AddField(
            model_name='offering',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='support.OfferingPlan'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-08 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openstack_tenant', '0038_internal_ip_settings_non_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalip',
            name='backend_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

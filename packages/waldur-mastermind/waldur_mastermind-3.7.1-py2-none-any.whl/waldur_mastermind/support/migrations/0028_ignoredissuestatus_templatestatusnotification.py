# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-23 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import waldur_core.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0027_non_unique_template_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='IgnoredIssueStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, validators=[waldur_core.core.validators.validate_name], verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='TemplateStatusNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255, unique=True, validators=[waldur_core.core.validators.validate_name])),
                ('html', models.TextField(validators=[waldur_core.core.validators.validate_name])),
                ('text', models.TextField(validators=[waldur_core.core.validators.validate_name])),
                ('subject', models.CharField(max_length=255, validators=[waldur_core.core.validators.validate_name])),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-14 00:19
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0014_add_accounting_start_date'),
        ('support', '0010_add_unit_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='offeringitem',
            name='unit',
            field=models.CharField(
                choices=[(b'month', 'Per month'),
                         (b'half_month', 'Per half month'),
                         (b'day', 'Per day'),
                         (b'quantity', 'Quantity')],
                default=b'day', max_length=30),
        ),
        migrations.AddField(
            model_name='openstackitem',
            name='unit',
            field=models.CharField(
                choices=[(b'month', 'Per month'),
                         (b'half_month', 'Per half month'),
                         (b'day', 'Per day'),
                         (b'quantity', 'Quantity')],
                default=b'day', max_length=30),
        ),
        migrations.AddField(
            model_name='offeringitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=7, default=0, max_digits=22,
                                      validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AddField(
            model_name='openstackitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=7, default=0, max_digits=22,
                                      validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]

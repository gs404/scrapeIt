# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-12-14 22:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraped', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='responses',
            new_name='Response',
        ),
    ]

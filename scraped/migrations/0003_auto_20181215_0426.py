# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-12-14 22:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraped', '0002_auto_20181215_0413'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]

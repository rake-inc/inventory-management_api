# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-21 06:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171121_0652'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Roles',
            new_name='Role',
        ),
    ]

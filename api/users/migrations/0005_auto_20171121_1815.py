# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-21 18:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20171121_0654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='department_manager',
            new_name='is_department_manager',
        ),
        migrations.RenameField(
            model_name='role',
            old_name='store_manager',
            new_name='is_store_manager',
        ),
        migrations.RenameField(
            model_name='roleapproval',
            old_name='approval',
            new_name='is_approved',
        ),
    ]

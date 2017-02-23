# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0009_django_cleanup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicanttype',
            name='active',
        ),
        migrations.RemoveField(
            model_name='applicanttype',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='active',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='jobcategory',
            name='active',
        ),
        migrations.RemoveField(
            model_name='jobcategory',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='location',
            name='active',
        ),
        migrations.RemoveField(
            model_name='location',
            name='slug',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, blank=True)),
                ('organization', models.CharField(max_length=250, blank=True)),
                ('email', models.EmailField(max_length=250, blank=True)),
                ('sessions', models.TextField()),
                ('foodinfo', models.CharField(max_length=250, blank=True)),
                ('accommodations', models.CharField(max_length=250, blank=True)),
                ('codes', models.TextField()),
            ],
        ),
    ]

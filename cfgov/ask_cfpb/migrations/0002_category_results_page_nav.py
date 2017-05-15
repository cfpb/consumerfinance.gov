# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answercategorypage',
            name='secondary_nav_exclude_sibling_pages',
        ),
        migrations.AddField(
            model_name='answerresultspage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([], null=True),
        ),
        migrations.AlterField(
            model_name='answercategorypage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([], null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('workflow', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflowdestinationsetting',
            name='is_destination',
        ),
        migrations.AddField(
            model_name='workflowdestinationsetting',
            name='destination',
            field=models.ForeignKey(related_name='workflow_destination', default=None, to='wagtailcore.Site', null=True),
        ),
    ]

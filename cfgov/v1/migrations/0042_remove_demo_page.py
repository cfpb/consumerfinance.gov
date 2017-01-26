# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('v1', '0041_create_html_block'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demopage',
            name='cfgovpage_ptr',
        ),
        migrations.RemoveField(
            model_name='demopage',
            name='contact',
        ),
        migrations.DeleteModel(
            name='DemoPage',
        ),
    ]

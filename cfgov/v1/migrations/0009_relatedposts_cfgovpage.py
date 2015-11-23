# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0008_auto_20151120_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovpage',
            name='is_relating_events',
            field=models.BooleanField(default=True, verbose_name=b'Events'),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='is_relating_newsroom',
            field=models.BooleanField(default=True, verbose_name=b'Newsroom'),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='is_relating_posts',
            field=models.BooleanField(default=True, verbose_name=b'Blog Posts'),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='related_limit',
            field=models.IntegerField(default=3, help_text=b'Limits results per type.', verbose_name=b'Limit'),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='view_more_label',
            field=models.CharField(default=b'View More', max_length=40),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='view_more_url',
            field=models.CharField(default=b'/', help_text=b'URL to additional related content.', max_length=200),
        ),
    ]

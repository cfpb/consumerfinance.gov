# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0061_make_info_unit_headings_linkable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='live_stream_url',
            field=models.URLField(blank=True, help_text=b'Format: https://www.ustream.tv/embed/video_id or https://www.youtube.com/embed/video_id.', verbose_name=b'URL', validators=[django.core.validators.RegexValidator(regex=b'^https?:\\/\\/www\\.(ustream\\.tv|youtube\\.com)\\/embed\\/.*$')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0085_auto_20160519_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='live_stream_url',
            field=models.URLField(blank=True, help_text=b'Format: https://www.ustream.tv/embed/video_id.  It can be obtained by following the instructions listed here: https://support.ustream.tv/hc/en-us/articles/207851917-How-to-embed-a-stream-or-video-on-your-site', verbose_name=b'URL', validators=[django.core.validators.RegexValidator(regex=b'^https?:\\/\\/www\\.ustream\\.tv\\/embed\\/.*$')]),
        ),
    ]

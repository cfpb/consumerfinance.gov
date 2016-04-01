# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0072_auto_20160331_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='youtube_url',
            field=models.URLField(blank=True, help_text=b'Format: https://www.youtube.com/embed/video_id. It can be obtained by clicking on Share > Embed on Youtube.', verbose_name=b'Youtube URL', validators=[django.core.validators.RegexValidator(regex=b'^https?:\\/\\/www\\.youtube\\.com\\/embed\\/.*$')]),
        ),
    ]

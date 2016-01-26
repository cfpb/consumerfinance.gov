# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0034_failedloginattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovpage',
            name='language',
            field=models.CharField(default=b'en', max_length=2, choices=[(b'en', b'English'), (b'es', b'Spanish'), (b'zh', b'Chinese'), (b'vi', b'Vietnamese'), (b'ko', b'Korean'), (b'tl', b'Tagalog'), (b'ru', b'Russian'), (b'ar', b'Arabic'), (b'ht', b'Haitian Creole')]),
        ),
    ]

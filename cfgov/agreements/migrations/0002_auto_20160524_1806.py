# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreement',
            name='effective_date',
        ),
        migrations.RemoveField(
            model_name='agreement',
            name='pdf_size',
        ),
        migrations.RemoveField(
            model_name='agreement',
            name='pdf_uri',
        ),
        migrations.RemoveField(
            model_name='agreement',
            name='txt_size',
        ),
        migrations.RemoveField(
            model_name='agreement',
            name='txt_uri',
        ),
        migrations.RemoveField(
            model_name='issuer',
            name='city',
        ),
        migrations.RemoveField(
            model_name='issuer',
            name='ffiec_regulator',
        ),
        migrations.RemoveField(
            model_name='issuer',
            name='state',
        ),
        migrations.AddField(
            model_name='agreement',
            name='size',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agreement',
            name='uri',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]

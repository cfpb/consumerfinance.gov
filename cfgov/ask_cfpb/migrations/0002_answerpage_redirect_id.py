# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerpage',
            name='redirect_id',
            field=models.IntegerField(help_text='Enter an Answer ID to redirect this page to', null=True, blank=True),
        ),
    ]

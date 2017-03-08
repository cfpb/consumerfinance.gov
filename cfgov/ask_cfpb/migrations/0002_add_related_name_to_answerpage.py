# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerpage',
            name='answer_base',
            field=models.ForeignKey(related_name='answer_pages', on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.Answer', null=True),
        ),
    ]

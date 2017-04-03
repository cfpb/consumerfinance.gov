# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0002_answerpage_redirect_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answerpage',
            name='redirect_id',
        ),
        migrations.AddField(
            model_name='answerpage',
            name='redirect_to',
            field=models.ForeignKey(related_name='redirected_pages', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ask_cfpb.Answer', help_text='Choose another Answer to redirect this page to', null=True),
        ),
        migrations.AlterField(
            model_name='answerpage',
            name='answer_base',
            field=models.ForeignKey(related_name='answer_pages', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ask_cfpb.Answer', null=True),
        ),
    ]

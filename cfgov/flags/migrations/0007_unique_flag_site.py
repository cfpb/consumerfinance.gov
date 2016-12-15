# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flags', '0006_auto_20151217_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flagstate',
            name='flag',
            field=models.ForeignKey(related_name='states', to='flags.Flag'),
        ),
        migrations.AlterField(
            model_name='flagstate',
            name='site',
            field=models.ForeignKey(related_name='flag_states', to='wagtailcore.Site'),
        ),
        migrations.AlterUniqueTogether(
            name='flagstate',
            unique_together=set([('flag', 'site')]),
        ),
    ]

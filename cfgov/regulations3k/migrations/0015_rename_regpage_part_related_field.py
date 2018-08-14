# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0014_rm_imageinset_and_media_from_fullwidthtext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulationpage',
            name='regulation',
            field=models.ForeignKey(related_name='page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='regulations3k.Part', null=True),
        ),
    ]

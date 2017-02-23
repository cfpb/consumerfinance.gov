# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('v1', '0002_share_perms'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovimage',
            name='collection',
            field=models.ForeignKey(related_name='+', default=wagtail.wagtailcore.models.get_root_collection_id, verbose_name='collection', to='wagtailcore.Collection'),
        ),
    ]

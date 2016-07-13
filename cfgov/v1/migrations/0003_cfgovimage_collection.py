# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('v1', '0002_create_share_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfgovimage',
            name='collection',
            field=models.ForeignKey(related_name='+', default=wagtail.wagtailcore.models.get_root_collection_id, verbose_name='collection', to='wagtailcore.Collection'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from v1.models.learn_page import DocumentDetailPage

class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0055_auto_20160224_2201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='abstractfilterpage',
            old_name='preview_link_text',
            new_name='secondary_link_text',
        ),
        migrations.RenameField(
            model_name='abstractfilterpage',
            old_name='preview_link_url',
            new_name='secondary_link_url',
        ),
    ]

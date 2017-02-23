# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailimages.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0003_cfgovimage_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cfgovrendition',
            name='file',
            field=models.ImageField(height_field='height', width_field='width', upload_to=wagtail.wagtailimages.models.get_rendition_upload_to),
        ),
    ]

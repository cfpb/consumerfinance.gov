# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobmanager', '0014_add_city_and_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobcategory',
            name='blurb',
            field=wagtail.wagtailcore.fields.RichTextField(null=True, blank=True),
        ),
    ]

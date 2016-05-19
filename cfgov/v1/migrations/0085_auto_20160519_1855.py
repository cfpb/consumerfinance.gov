# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0084_auto_20160510_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(verbose_name=b'Subheading', blank=True),
        ),
    ]

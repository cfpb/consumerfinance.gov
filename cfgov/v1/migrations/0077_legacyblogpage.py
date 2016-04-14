# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0076_auto_20160405_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegacyBlogPage',
            fields=[
                ('abstractfilterpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.AbstractFilterPage')),
                ('content', wagtail.wagtailcore.fields.RichTextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.abstractfilterpage',),
        ),
    ]

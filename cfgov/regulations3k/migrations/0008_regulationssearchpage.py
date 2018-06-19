# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.contrib.wagtailroutablepage.models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0113_modify_help_text_social_sharing_image'),
        ('regulations3k', '0007_make_sortable_label_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegulationsSearchPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'v1.cfgovpage'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0051_abstractfilterpage_preview_link_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.RemoveField(
            model_name='browsepage',
            name='side_navigation',
        ),
    ]

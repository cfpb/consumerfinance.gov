# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0078_newsroomlandingpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegacyNewsroomPage',
            fields=[
                ('legacyblogpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.LegacyBlogPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.legacyblogpage',),
        ),
    ]

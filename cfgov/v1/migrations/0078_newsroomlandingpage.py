# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0077_legacyblogpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsroomLandingPage',
            fields=[
                ('browsefilterablepage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.BrowseFilterablePage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.browsefilterablepage',),
        ),
    ]

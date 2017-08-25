# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0087_add_mortgage_chart_block_to_browsepage'),
        ('data_research', '0005_mortgagemetadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='MortgagePerformancePage',
            fields=[
                ('browsepage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.BrowsePage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.browsepage',),
        ),
    ]

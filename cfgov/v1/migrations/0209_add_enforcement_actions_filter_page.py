# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0208_job_listing_block_refactor'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnforcementActionsFilterPage',
            fields=[
                ('browsefilterablepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='v1.BrowseFilterablePage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.browsefilterablepage',),
        ),
    ]

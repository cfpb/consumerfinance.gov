# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youth_activity_search', '0008_auto_20180718_1428'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityindexpage',
            options={'verbose_name': 'Youth Activity search page'},
        ),
        migrations.AlterModelOptions(
            name='activitypage',
            options={'verbose_name': 'Youth Activity page'},
        ),
    ]

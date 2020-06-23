# -*- coding: utf-8 -*-
from django.db import migrations, models
import youth_activity_search.fields


class Migration(migrations.Migration):

    dependencies = [
        ('youth_activity_search', '0006_auto_20180704_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitypage',
            name='topic',
            field=youth_activity_search.fields.ParentalTreeManyToManyField(to='youth_activity_search.ActivityTopic'),
        ),
    ]

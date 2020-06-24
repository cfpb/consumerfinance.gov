# -*- coding: utf-8 -*-
from django.db import migrations, models
import mptt.fields
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('youth_activity_search', '0005_auto_20180703_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitypage',
            name='council_for_economic_education',
            field=modelcluster.fields.ParentalManyToManyField(to='youth_activity_search.ActivityCouncilForEconEd', verbose_name='Council for Economic Education', blank=True),
        ),
        migrations.AlterField(
            model_name='activitypage',
            name='jump_start_coalition',
            field=modelcluster.fields.ParentalManyToManyField(to='youth_activity_search.ActivityJumpStartCoalition', verbose_name='Jump$tart Coalition', blank=True),
        ),
        migrations.AlterField(
            model_name='activitypage',
            name='topic',
            field=mptt.fields.TreeManyToManyField(to='youth_activity_search.ActivityTopic'),
        ),
    ]

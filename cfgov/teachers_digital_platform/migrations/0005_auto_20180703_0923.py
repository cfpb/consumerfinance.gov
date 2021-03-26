# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0004_auto_20180703_0825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityagerange',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activitybloomstaxonomylevel',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activitybuildingblock',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activitycouncilforeconed',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activityduration',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activitygradelevel',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activityjumpstartcoalition',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activityschoolsubject',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activityspecialpopulation',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activityteachingstrategy',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AlterModelOptions(
            name='activitytype',
            options={'ordering': ['weight', 'title']},
        ),
        migrations.AddField(
            model_name='activityagerange',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activitybloomstaxonomylevel',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activitybuildingblock',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activitycouncilforeconed',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activityduration',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activitygradelevel',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activityjumpstartcoalition',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activityschoolsubject',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activityspecialpopulation',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activityteachingstrategy',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activitytopic',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activitytype',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0003_auto_20180702_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitysubtopic',
            name='parent',
        ),
        migrations.AlterModelOptions(
            name='activitytopic',
            options={},
        ),
        migrations.AddField(
            model_name='activitytopic',
            name='level',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activitytopic',
            name='lft',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activitytopic',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='teachers_digital_platform.ActivityTopic', null=True),
        ),
        migrations.AddField(
            model_name='activitytopic',
            name='rght',
            field=models.PositiveIntegerField(default=0, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activitytopic',
            name='tree_id',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ActivitySubTopic',
        ),
    ]

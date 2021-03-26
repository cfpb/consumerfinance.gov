# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0002_activitysubtopic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityagerange',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activitybloomstaxonomylevel',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activitybuildingblock',
            name='icon',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', null=True),
        ),
        migrations.AlterField(
            model_name='activitybuildingblock',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activitycouncilforeconed',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activityduration',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activitygradelevel',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activityjumpstartcoalition',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activityschoolsubject',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activityspecialpopulation',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activitysubtopic',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activityteachingstrategy',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activitytopic',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activitytype',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]

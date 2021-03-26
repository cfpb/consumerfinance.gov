# -*- coding: utf-8 -*-
from django.db import migrations, models
from wagtail.core import fields as core_fields
import modelcluster.fields
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('v1', '0198_recreated'),
        ('wagtailimages', '0019_delete_filter'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityAgeRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityBloomsTaxonomyLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityBuildingBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('icon', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityCouncilForEconEd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityDuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityGradeLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityIndexPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage', on_delete=django.db.models.deletion.SET_NULL)),
                ('intro', core_fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='ActivityJumpStartCoalition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage', on_delete=django.db.models.deletion.SET_NULL)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('summary', models.TextField(verbose_name='Summary')),
                ('big_idea', core_fields.RichTextField(verbose_name='Big idea')),
                ('essential_questions', core_fields.RichTextField(verbose_name='Essential questions')),
                ('objectives', core_fields.RichTextField(verbose_name='Objectives')),
                ('what_students_will_do', core_fields.RichTextField(verbose_name='What students will do')),
                ('activity_duration', models.ForeignKey(to='teachers_digital_platform.ActivityDuration', on_delete=django.db.models.deletion.PROTECT)),
                ('activity_file', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.Document', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='ActivitySchoolSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivitySpecialPopulation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityTeachingStrategy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activitypage',
            name='activity_type',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityType'),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='age_range',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityAgeRange'),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='blooms_taxonomy_level',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityBloomsTaxonomyLevel'),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='building_block',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityBuildingBlock'),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='council_for_economic_education',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityCouncilForEconEd', blank=True),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='grade_level',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityGradeLevel'),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='handout_file',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='jump_start_coalition',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityJumpStartCoalition', blank=True),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='school_subject',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivitySchoolSubject'),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='special_population',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivitySpecialPopulation', blank=True),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='teaching_strategy',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityTeachingStrategy'),
        ),
        migrations.AddField(
            model_name='activitypage',
            name='topic',
            field=modelcluster.fields.ParentalManyToManyField(to='teachers_digital_platform.ActivityTopic'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import taggit.managers
import modelcluster.fields
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('taggit', '0002_auto_20150616_2121'),
        ('v1', '0019_modify_fcm_help'),
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('desc', wagtail.wagtailcore.fields.RichTextField(verbose_name=b'Description', blank=True)),
                ('order_link', models.URLField(blank=True, help_text=b'URL to order a few copies of aprinted piece.', validators=[django.core.validators.URLValidator])),
                ('bulk_order_link', models.URLField(blank=True, help_text=b'URL to order copies of aprinted piece in bulk.', validators=[django.core.validators.URLValidator])),
                ('hash', models.CharField(max_length=32, editable=False)),
                ('related_file', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
                ('related_file_es', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DownloadTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', modelcluster.fields.ParentalKey(related_name='tagged_items', to='v1.Download')),
                ('tag', models.ForeignKey(related_name='v1_downloadtag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='download',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='v1.DownloadTag', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='download',
            name='thumbnail',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('v1', '0002_create_event_pages'),
    ]

    operations = [
        migrations.CreateModel(
            name='CFGOVAuthoredPages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', modelcluster.fields.ParentalKey(to='v1.CFGOVPage')),
                ('tag', models.ForeignKey(related_name='v1_cfgovauthoredpages_items', to='taggit.Tag')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='CFGOVTaggedPages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', modelcluster.fields.ParentalKey(to='v1.CFGOVPage')),
                ('tag', models.ForeignKey(related_name='v1_cfgovtaggedpages_items', to='taggit.Tag')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='agenda_items',
            field=wagtail.wagtailcore.fields.StreamField([(b'item', wagtail.wagtailcore.blocks.StructBlock([(b'start_dt', wagtail.wagtailcore.blocks.DateTimeBlock(required=False, label=b'Start')), (b'end_dt', wagtail.wagtailcore.blocks.DateTimeBlock(required=False, label=b'End')), (b'description', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'location', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'speakers', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'name', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.URLBlock(required=False))], required=False, icon=b'user')))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='end_dt',
            field=models.DateTimeField(null=True, verbose_name=b'End', blank=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='start_dt',
            field=models.DateTimeField(null=True, verbose_name=b'Start', blank=True),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='authors',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='v1.CFGOVAuthoredPages', blank=True, help_text=b'A comma separated list of authors.', verbose_name=b'Authors'),
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='v1.CFGOVTaggedPages', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]

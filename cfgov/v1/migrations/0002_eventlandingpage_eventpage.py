# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
import wagtail.wagtailcore.fields
import django.db.models.deletion
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('wagtaildocs', '0003_add_verbose_names'),
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLandingPage',
            fields=[
                ('v1page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.V1Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.v1page',),
        ),
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('v1page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.V1Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('archive_body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('live_body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('start_dt', models.DateField(null=True, verbose_name=b'Starts', blank=True)),
                ('end_dt', models.DateField(null=True, verbose_name=b'Ends', blank=True)),
                ('future_body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('flickr_url', models.URLField(verbose_name=b'Flikr URL', blank=True)),
                ('youtube_url', models.URLField(verbose_name=b'Youtube URL', blank=True)),
                ('live_stream_availability', models.BooleanField(default=False, verbose_name=b'Streaming?')),
                ('live_stream_url', models.URLField(verbose_name=b'URL', blank=True)),
                ('live_stream_date', models.DateField(null=True, verbose_name=b'Go Live Date', blank=True)),
                ('venue_name', models.CharField(max_length=100, blank=True)),
                ('venue_street', models.CharField(max_length=100, blank=True)),
                ('venue_suite', models.CharField(max_length=100, blank=True)),
                ('venue_city', models.CharField(max_length=100, blank=True)),
                ('venue_state', localflavor.us.models.USStateField(blank=True, max_length=2, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('venue_zip', models.IntegerField(null=True, blank=True)),
                ('agenda_items', wagtail.wagtailcore.fields.StreamField([(b'item', wagtail.wagtailcore.blocks.StructBlock([(b'start_dt', wagtail.wagtailcore.blocks.DateTimeBlock(required=False, format=b'%Y-%m-%d %H:%M')), (b'end_dt', wagtail.wagtailcore.blocks.DateTimeBlock(required=False, format=b'%Y-%m-%d %H:%M')), (b'description', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'location', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'speakers', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'name', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.URLBlock(required=False))], required=False, icon=b'user')))]))], blank=True)),
                ('archive_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
                ('speech_transcript', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
                ('video_transcript', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtaildocs.Document', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.v1page',),
        ),
    ]

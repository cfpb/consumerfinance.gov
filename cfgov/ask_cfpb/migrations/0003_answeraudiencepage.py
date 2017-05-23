# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import django.db.models.deletion
import v1.feeds
import v1.util.filterable_list


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0066_fix_for_linking_video_stills'),
        ('ask_cfpb', '0002_category_results_page_nav'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerAudiencePage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('content', wagtail.wagtailcore.fields.StreamField([], null=True)),
                ('ask_audience', models.ForeignKey(related_name='audience_page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.Audience', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(v1.feeds.FilterableFeedPageMixin, v1.util.filterable_list.FilterableListMixin, 'v1.cfgovpage'),
        ),
    ]

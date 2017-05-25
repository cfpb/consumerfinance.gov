# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0067_auto_20170517_1344'),
        ('ask_cfpb', '0001_initial'),
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
            bases=('v1.cfgovpage',),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0004_eventarchivepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRequestSpeakerPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('header', models.CharField(max_length=100)),
                ('intro', models.TextField(verbose_name=b'Introduction', blank=True)),
                ('subpage_desc', wagtail.wagtailcore.fields.RichTextField(verbose_name=b'Subpage description', blank=True)),
                ('faq', wagtail.wagtailcore.fields.StreamField([(b'Heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'full title')), (b'Description', wagtail.wagtailcore.blocks.TextBlock()), (b'QA', wagtail.wagtailcore.blocks.StructBlock([(b'question', wagtail.wagtailcore.blocks.CharBlock()), (b'answer', wagtail.wagtailcore.blocks.CharBlock())]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
    ]

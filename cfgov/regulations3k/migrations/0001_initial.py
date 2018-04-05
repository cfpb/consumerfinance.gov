# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.contrib.wagtailroutablepage.models
import wagtail.wagtailcore.fields
import regulations3k.models.fields
import django.db.models.deletion
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0102_recreated'),
    ]

    operations = [
        migrations.CreateModel(
            name='EffectiveVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authority', models.CharField(max_length=255, blank=True)),
                ('source', models.CharField(max_length=255, blank=True)),
                ('effecitve_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cfr_title', models.CharField(max_length=255)),
                ('chapter', models.CharField(max_length=255)),
                ('part_number', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('letter_code', models.CharField(max_length=10)),
                ('versions', models.ForeignKey(related_name='part_version', blank=True, to='regulations3k.EffectiveVersion', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegulationLandingPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='RegulationPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('regdown', regulations3k.models.fields.RegDownTextField(default='regdown text')),
                ('header', wagtail.wagtailcore.fields.StreamField([('text_introduction', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Check this to add a horizontal rule line to bottom of text introduction.', required=False, label=b'Has bottom rule'))]))], blank=True)),
                ('content', wagtail.wagtailcore.fields.StreamField([], null=True)),
                ('secondary_nav_exclude_sibling_pages', models.BooleanField(default=False)),
                ('regulation', models.ForeignKey(related_name='eregs3k_page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='regulations3k.Part', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'v1.cfgovpage'),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, blank=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('contents', regulations3k.models.fields.RegDownTextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subpart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, blank=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('sections', models.ForeignKey(blank=True, to='regulations3k.Section', null=True)),
                ('version', models.ForeignKey(related_name='subpart_version', blank=True, to='regulations3k.EffectiveVersion', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='effectiveversion',
            name='part',
            field=models.ForeignKey(blank=True, to='regulations3k.Part', null=True),
        ),
        migrations.AddField(
            model_name='effectiveversion',
            name='subparts',
            field=models.ForeignKey(blank=True, to='regulations3k.Subpart', null=True),
        ),
    ]

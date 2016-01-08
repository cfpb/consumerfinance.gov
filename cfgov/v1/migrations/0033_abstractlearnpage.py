# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0032_cfgovimage_cfgovrendition'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractLearnPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('header', wagtail.wagtailcore.fields.StreamField([(b'text_introduction', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(required=False))])), (b'item_introduction', wagtail.wagtailcore.blocks.StructBlock([(b'category', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=[(b'info for consumers', b'Info for consumers'), (b'at the cfpb', b'At the CFPB'), (b'data, research & reports', b'Data, research & reports'), (b'policy & compliance', b'Policy & Compliance'), (b'speech', b'Speech'), (b'press release', b'Press Release'), (b'op-ed', b'Op-ed'), (b'testimony', b'Testimony'), (b'cfpb_report', b'CFPB Report'), (b'blog', b'Blog'), (b'newsroom', b'Newsroom')])), (b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'authors', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))), (b'date', wagtail.wagtailcore.blocks.DateTimeBlock(required=False)), (b'has_social', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Whether to show the share icons or not.', required=False))]))], blank=True)),
                ('preview_title', models.CharField(max_length=255, null=True, blank=True)),
                ('preview_subheading', models.CharField(max_length=255, null=True, blank=True)),
                ('preview_description', wagtail.wagtailcore.fields.RichTextField(null=True, blank=True)),
                ('preview_link_text', models.CharField(max_length=255, null=True, blank=True)),
                ('date_published', models.DateField()),
                ('date_filed', models.DateField(null=True, blank=True)),
                ('comments_close_by', models.DateField(null=True, blank=True)),
                ('preview_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.RemoveField(
            model_name='documentdetailpage',
            name='cfgovpage_ptr',
        ),
        migrations.RemoveField(
            model_name='documentdetailpage',
            name='header',
        ),
        migrations.RemoveField(
            model_name='learnpage',
            name='cfgovpage_ptr',
        ),
        migrations.RemoveField(
            model_name='learnpage',
            name='header',
        ),
        migrations.AddField(
            model_name='documentdetailpage',
            name='abstractlearnpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='v1.AbstractLearnPage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='learnpage',
            name='abstractlearnpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=2, serialize=False, to='v1.AbstractLearnPage'),
            preserve_default=False,
        ),
    ]

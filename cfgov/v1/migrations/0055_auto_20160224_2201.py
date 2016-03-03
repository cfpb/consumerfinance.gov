# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


def migrate_text_intro_blocks(apps, schema_editor):
    SublandingPage = apps.get_model('v1.SublandingPage')
    PageRevision = apps.get_model('wagtailcore.PageRevision')

    for page in SublandingPage.objects.all():
        for i, child in enumerate(page.header.stream_data):
            if child['type'] == 'text_introduction':
                page.content.stream_data = [child] + page.content.stream_data
                del page.header.stream_data[i]
                page.save()
        revisions = PageRevision.objects.filter(page=page).order_by('-id')
        latest_revision = revisions.first()
        revisions_to_update = {'shared': None, 'live': None}
        for attr in revisions_to_update.keys():
            for revision in revisions:
                content = json.loads(revision.content_json)
                if content[attr]:
                    revisions_to_update[attr] = revision
        revisions_to_update.update({'latest': latest_revision})
        page_content = json.loads(latest_revision.content_json)
        header = json.loads(page_content['header'])
        content = json.loads(page_content['content'])
        for i, child in enumerate(header):
            if child['type'] == 'text_introduction':
                content += [child]
                del header[i]
        page_content['header'] = json.dumps(header)
        page_content['content'] = json.dumps(content)
        content = json.dumps(page_content)
        for revision in revisions_to_update.values():
            if revision:
                revision.content_json = content
                revision.save()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0054_auto_20160229_2044'),
    ]

    operations = [
        migrations.RunPython(migrate_text_intro_blocks),
        migrations.AlterField(
            model_name='sublandingpage',
            name='header',
            field=wagtail.wagtailcore.fields.StreamField([(b'hero', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), (b'alt', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'background_color', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Use Hexcode colors e.g #F0F8FF', required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))), (b'is_button', wagtail.wagtailcore.blocks.BooleanBlock(required=False))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='sublandingpage',
            name='sidebar_breakout',
            field=wagtail.wagtailcore.fields.StreamField([(b'slug', wagtail.wagtailcore.blocks.CharBlock(icon=b'title')), (b'heading', wagtail.wagtailcore.blocks.CharBlock(icon=b'title')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon=b'edit')), (b'breakout_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'is_round', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Round?')), (b'icon', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Enter icon class name.')), (b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False, label=b'Introduction Heading')), (b'body', wagtail.wagtailcore.blocks.TextBlock(required=False, label=b'Introduction Body'))], heading=b'Breakout Image', icon=b'image')), (b'related_posts', wagtail.wagtailcore.blocks.StructBlock([(b'limit', wagtail.wagtailcore.blocks.CharBlock(default=b'3', label=b'Limit')), (b'show_heading', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'This toggles the heading and icon for the related types.', default=True, required=False, label=b'Show Heading and Icon?')), (b'relate_posts', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, editable=False, label=b'Blog Posts')), (b'relate_newsroom', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, editable=False, label=b'Newsroom')), (b'relate_events', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Events')), (b'view_more', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))]))], blank=True),
        ),
    ]

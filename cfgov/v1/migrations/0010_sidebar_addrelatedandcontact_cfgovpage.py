# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailsnippets.blocks
import v1.models.snippets
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0009_auto_20151125_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landingpage',
            name='sidebar',
        ),
        migrations.AddField(
            model_name='cfgovpage',
            name='sidefoot',
            field=wagtail.wagtailcore.fields.StreamField([(b'slug', wagtail.wagtailcore.blocks.CharBlock()), (b'heading', wagtail.wagtailcore.blocks.CharBlock()), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'hyperlink', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])), (b'call_to_action', wagtail.wagtailcore.blocks.StructBlock([(b'slug_text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'paragraph_text', wagtail.wagtailcore.blocks.RichTextBlock(required=True)), (b'button', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))])), (b'related_posts', wagtail.wagtailcore.blocks.StructBlock([(b'limit', wagtail.wagtailcore.blocks.CharBlock(default=b'3', label=b'Limit')), (b'relate_posts', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Blog Posts')), (b'relate_newsroom', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Newsroom')), (b'relate_events', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Events')), (b'view_more', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))])), (b'email_signup', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'text', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'gd_code', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'form_field', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'btn_text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'required', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'id', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'info', wagtail.wagtailcore.blocks.RichTextBlock(required=False, label=b'Disclaimer')), (b'label', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'type', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'text', b'Text'), (b'checkbox', b'Checkbox'), (b'email', b'Email'), (b'number', b'Number'), (b'url', b'URL'), (b'radio', b'Radio')])), (b'placeholder', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False))]), required=False, icon=b'mail'))])), (b'contact', wagtail.wagtailcore.blocks.StructBlock([(b'header', wagtail.wagtailcore.blocks.CharBlock()), (b'body', wagtail.wagtailcore.blocks.RichTextBlock()), (b'contact', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(v1.models.snippets.Contact))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='demopage',
            name='organisms',
            field=wagtail.wagtailcore.fields.StreamField([(b'well', wagtail.wagtailcore.blocks.StructBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(required=True))])), (b'full_width_text', wagtail.wagtailcore.blocks.StructBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(required=True))])), (b'post_preview', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=True)), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'upload', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))])), (b'post', wagtail.wagtailcore.blocks.PageChooserBlock(required=True)), (b'link', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))]))], blank=True),
        ),
    ]

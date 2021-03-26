# -*- coding: utf-8 -*-
from django.db import migrations
from wagtail.core import blocks as core_blocks
from wagtail.core import fields as core_fields


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0019_activitybuildingblock_svg_icon_labels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityindexpage',
            name='intro',
        ),
        migrations.AddField(
            model_name='activityindexpage',
            name='header',
            field=core_fields.StreamField([('text_introduction', core_blocks.StructBlock([('eyebrow', core_blocks.CharBlock(help_text='Optional: Adds an H5 eyebrow above H1 heading text. Only use in conjunction with heading.', label='Pre-heading', required=False)), ('heading', core_blocks.CharBlock(required=False)), ('intro', core_blocks.RichTextBlock(required=False)), ('body', core_blocks.RichTextBlock(required=False)), ('links', core_blocks.ListBlock(core_blocks.StructBlock([('text', core_blocks.CharBlock(required=False)), ('url', core_blocks.CharBlock(default='/', required=False))]), required=False)), ('has_rule', core_blocks.BooleanBlock(help_text='Check this to add a horizontal rule line to bottom of text introduction.', label='Has bottom rule', required=False))]))], blank=True),
        ),
    ]

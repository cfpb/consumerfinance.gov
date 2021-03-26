# -*- coding: utf-8 -*-
from django.db import migrations
from wagtail.core import blocks as core_blocks
from wagtail.core import fields as core_fields
from wagtail.images import blocks as images_blocks


class Migration(migrations.Migration):

    dependencies = [
        ('teachers_digital_platform', '0020_activityindexpage_text_introduction'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityindexpage',
            name='header_sidebar',
            field=core_fields.StreamField([('image', core_blocks.StructBlock([('image', images_blocks.ImageChooserBlock(help_text='Should be exactly 390px tall, and up to 940px wide, unless this is an overlay or bleeding style hero.')), ('small_image', images_blocks.ImageChooserBlock(help_text='Provide an alternate image for small displays when using a bleeding or overlay hero.', required=False))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='activityindexpage',
            name='header',
            field=core_fields.StreamField([('text_introduction', core_blocks.StructBlock([('eyebrow', core_blocks.CharBlock(help_text='Optional: Adds an H5 eyebrow above H1 heading text. Only use in conjunction with heading.', label='Pre-heading', required=False)), ('heading', core_blocks.CharBlock(required=False)), ('intro', core_blocks.RichTextBlock(required=False)), ('body', core_blocks.RichTextBlock(required=False)), ('links', core_blocks.ListBlock(core_blocks.StructBlock([('text', core_blocks.CharBlock(required=False)), ('url', core_blocks.CharBlock(default='/', required=False))]), required=False)), ('has_rule', core_blocks.BooleanBlock(help_text='Check this to add a horizontal rule line to bottom of text introduction.', label='Has bottom rule', required=False))])), ('notification', core_blocks.StructBlock([('message', core_blocks.CharBlock(help_text='The main notification message to display.', required=True)), ('explanation', core_blocks.TextBlock(help_text='Explanation text appears below the message in smaller type.', required=False)), ('links', core_blocks.ListBlock(core_blocks.StructBlock([('text', core_blocks.CharBlock(required=False)), ('url', core_blocks.CharBlock(default='/', required=False))]), help_text='Links appear on their own lines below the explanation.', required=False))]))], blank=True),
        ),
    ]

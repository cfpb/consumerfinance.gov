# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0005_eventarchivepage_eventrequestspeakerpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(max_length=22)),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('contact_info', wagtail.wagtailcore.fields.StreamField(
                    [
                        (b'email', wagtail.wagtailcore.blocks.StructBlock(
                            [
                                (b'emails', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock(
                                        [
                                            (b'label', wagtail.wagtailcore.blocks.CharBlock(max_length=22)),
                                            (b'href', wagtail.wagtailcore.blocks.CharBlock(default=b'/'))
                                        ], label=b'Email')))
                            ])
                        ),
                        (b'phone', wagtail.wagtailcore.blocks.StructBlock(
                            [
                                (b'fax', wagtail.wagtailcore.blocks.BooleanBlock(default=False, required=False, label=b'Fax?')),
                                (b'phones', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock(
                                    [
                                        (b'number', wagtail.wagtailcore.blocks.CharBlock(max_length=15)),
                                        (b'vanity', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False)),
                                        (b'tty', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False))
                                    ]))
                                )
                            ])
                        ),
                        (b'address', wagtail.wagtailcore.blocks.StructBlock(
                            [
                                (b'label', wagtail.wagtailcore.blocks.CharBlock(max_length=50)),
                                (b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)),
                                (b'street', wagtail.wagtailcore.blocks.CharBlock(max_length=100)),
                                (b'city', wagtail.wagtailcore.blocks.CharBlock(max_length=50)),
                                (b'state', wagtail.wagtailcore.blocks.CharBlock(max_length=25)),
                                (b'zip_code', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False))
                            ])
                        )
                    ])
                ),
            ],
        ),
        migrations.AlterField(
            model_name='demopage',
            name='molecules',
            field=wagtail.wagtailcore.fields.StreamField(
                [
                    (b'half_width_link_blob', wagtail.wagtailcore.blocks.StructBlock(
                        [
                            (b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)),
                            (b'content', wagtail.wagtailcore.blocks.RichTextBlock(blank=True)),
                            (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock(
                                [
                                    (b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)),
                                    (b'url', wagtail.wagtailcore.blocks.URLBlock(required=False))
                                ], required=False, icon=b'user')))
                        ])
                    ),
                    (b'text_introduction', wagtail.wagtailcore.blocks.StructBlock(
                        [
                            (b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)),
                            (b'intro', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)),
                            (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)),
                            (b'link_url', wagtail.wagtailcore.blocks.URLBlock(required=False)),
                            (b'link_text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)),
                            (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(required=False))
                        ])
                    ),
                    (b'image_text_5050', wagtail.wagtailcore.blocks.StructBlock(
                        [
                            (b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)),
                            (b'description', wagtail.wagtailcore.blocks.RichTextBlock(blank=True)),
                            (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)),
                            (b'image_path', wagtail.wagtailcore.blocks.CharBlock(required=False)),
                            (b'image_alt', wagtail.wagtailcore.blocks.CharBlock(required=False)),
                            (b'is_widescreen', wagtail.wagtailcore.blocks.BooleanBlock(required=False)),
                            (b'is_button', wagtail.wagtailcore.blocks.BooleanBlock(required=False)),
                            (b'link_url', wagtail.wagtailcore.blocks.URLBlock(required=False)),
                            (b'link_text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False))
                        ])
                    )
                ], blank=True),
        ),
    ]

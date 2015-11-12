# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0006_contactsnippet_contactmolecules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact_info',
            field=wagtail.wagtailcore.fields.StreamField([(b'email', wagtail.wagtailcore.blocks.StructBlock([(b'emails', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'label', wagtail.wagtailcore.blocks.CharBlock(max_length=22)), (b'href', wagtail.wagtailcore.blocks.CharBlock(default=b'/'))], label=b'Email')))])), (b'phone', wagtail.wagtailcore.blocks.StructBlock([(b'fax', wagtail.wagtailcore.blocks.BooleanBlock(default=False, required=False, label=b'Is this number a fax?')), (b'phones', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'number', wagtail.wagtailcore.blocks.CharBlock(max_length=15)), (b'vanity', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False)), (b'tty', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False))])))])), (b'address', wagtail.wagtailcore.blocks.StructBlock([(b'label', wagtail.wagtailcore.blocks.CharBlock(max_length=50)), (b'title', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'street', wagtail.wagtailcore.blocks.CharBlock(max_length=100)), (b'city', wagtail.wagtailcore.blocks.CharBlock(max_length=50)), (b'state', wagtail.wagtailcore.blocks.CharBlock(max_length=25)), (b'zip_code', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='heading',
            field=models.CharField(help_text=b'The snippet heading', max_length=255, verbose_name=b'Heading'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='flickr_url',
            field=models.URLField(verbose_name=b'Flickr URL', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
import django.core.validators
import wagtail.core.blocks
import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0209_add_enforcement_actions_filter_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='For internal reference only; does not appear on the site.', max_length=255)),
                ('url_pattern', models.CharField(help_text='A regular expression pattern for matching URLs that should show the banner, for example: <code>contact-us|^/complaint/$</code>', max_length=1000, validators=[django.core.validators.RegexValidator(regex='[A-Za-z0-9\\-_.:/?&|\\^$]')], verbose_name='URL patterns')),
                ('content', wagtail.core.fields.StreamField([('content', wagtail.core.blocks.StructBlock([('message', wagtail.core.blocks.CharBlock(help_text='The main notification message to display.', required=True)), ('explanation', wagtail.core.blocks.TextBlock(help_text='Explanation text appears below the message in smaller type.', required=False)), ('links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=False)), ('url', wagtail.core.blocks.CharBlock(default='/', required=False))]), help_text='Links appear on their own lines below the explanation.', required=False))]))])),
                ('enabled', models.BooleanField()),
            ],
        ),
    ]

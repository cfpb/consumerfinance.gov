# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    replaces = [
        ('ask_cfpb', '0001_initial'),
        ('ask_cfpb', '0002_answeraudiencepage'),
        ('ask_cfpb', '0003_add_answercategorypage'),
        ('ask_cfpb', '0004_add_ask_category_images'),
        ('ask_cfpb', '0005_delete_answertagproxy'),
        ('ask_cfpb', '0006_update_help_text'),
        ('ask_cfpb', '0007_subcategory_prefixes'),
        ('ask_cfpb', '0008_fix_verbose_name_plural'),
        ('ask_cfpb', '0009_update_social_image_help_text'),
        ('ask_cfpb', '0010_answerpage_sidebar'),
        ('ask_cfpb', '0011_move_reusable_text_chooser_block'),
        ('ask_cfpb', '0012_add_rule_option_to_module'),
    ]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(blank=True)),
                ('statement', models.TextField(help_text='(Optional) Use this field to rephrase the question title as a statement. Use only if this answer has been chosen to appear on a money topic portal (e.g. /consumer-tools/debt-collection).', blank=True)),
                ('snippet', wagtail.wagtailcore.fields.RichTextField(help_text='Optional answer intro, 180-200 characters max. Avoid adding links, images, videos or other rich text elements.', blank=True)),
                ('answer', wagtail.wagtailcore.fields.RichTextField(help_text='Do not use H2 or H3 to style text. Only use the HTML Editor for troubleshooting. To style tips, warnings and notes, select the content that will go inside the rule lines (so, title + paragraph) and click the Pencil button to style it. Click again to unstyle the tip.', blank=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('featured', models.BooleanField(default=False, help_text='Check to make this one of two featured answers on the landing page.')),
                ('featured_rank', models.IntegerField(null=True, blank=True)),
                ('question_es', models.TextField(verbose_name='Spanish question', blank=True)),
                ('snippet_es', wagtail.wagtailcore.fields.RichTextField(help_text='Do not use this field. It is not currently displayed on the front end.', verbose_name='Spanish snippet', blank=True)),
                ('answer_es', wagtail.wagtailcore.fields.RichTextField(help_text='Do not use H2 or H3 to style text. Only use the HTML Editor for troubleshooting. Also note that tips styling (the Pencil button) does not display on the front end.', verbose_name='Spanish answer', blank=True)),
                ('slug_es', models.SlugField(max_length=255, verbose_name='Spanish slug', blank=True)),
                ('search_tags', models.CharField(help_text='Search words or phrases, separated by commas', max_length=1000, blank=True)),
                ('search_tags_es', models.CharField(help_text='Spanish search words or phrases, separated by commas', max_length=1000, blank=True)),
                ('update_english_page', models.BooleanField(default=False, help_text='Check this box to push your English edits to the page for review. This does not publish your edits.', verbose_name='Send to English page for review')),
                ('update_spanish_page', models.BooleanField(default=False, help_text='Check this box to push your Spanish edits to the page for review. This does not publish your edits.', verbose_name='Send to Spanish page for review')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_edited', models.DateField(help_text='Change the date to today if you edit an English question, snippet or answer.', null=True, verbose_name='Last edited English content', blank=True)),
                ('last_edited_es', models.DateField(help_text='Change the date to today if you edit a Spanish question, snippet or answer.', null=True, verbose_name='Last edited Spanish content', blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]

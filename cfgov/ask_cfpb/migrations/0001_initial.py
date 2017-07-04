# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(blank=True)),
                ('statement', models.TextField(help_text='Text to be used on portal pages to refer to this answer', blank=True)),
                ('snippet', wagtail.wagtailcore.fields.RichTextField(help_text='Optional answer intro', blank=True)),
                ('answer', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('featured', models.BooleanField(default=False, help_text='Makes the answer available to cards on the landing page')),
                ('featured_rank', models.IntegerField(null=True, blank=True)),
                ('question_es', models.TextField(verbose_name='Spanish question', blank=True)),
                ('snippet_es', wagtail.wagtailcore.fields.RichTextField(help_text='Optional Spanish answer intro', verbose_name='Spanish snippet', blank=True)),
                ('answer_es', wagtail.wagtailcore.fields.RichTextField(verbose_name='Spanish answer', blank=True)),
                ('slug_es', models.SlugField(max_length=255, verbose_name='Spanish slug', blank=True)),
                ('search_tags', models.CharField(help_text='Search words or phrases, separated by commas', max_length=1000, blank=True)),
                ('search_tags_es', models.CharField(help_text='Spanish search words or phrases, separated by commas', max_length=1000, blank=True)),
                ('update_english_page', models.BooleanField(default=False, verbose_name='Send to English page for review')),
                ('update_spanish_page', models.BooleanField(default=False, verbose_name='Send to Spanish page for review')),
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

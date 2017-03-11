# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ask_cfpb', '0002_add_related_name_to_answerpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_es',
            field=wagtail.wagtailcore.fields.RichTextField(verbose_name='Spanish answer', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='audiences',
            field=models.ManyToManyField(help_text='Pick any audiences that may be interested in the answer', to='ask_cfpb.Audience', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='category',
            field=models.ManyToManyField(help_text='This associates an answer with a portal page', to='ask_cfpb.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='last_edited',
            field=models.DateField(help_text='Change the date to today if you edit an English question, snippet or answer.', null=True, verbose_name='Last edited English content', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='last_edited_es',
            field=models.DateField(help_text='Change the date to today if you edit a Spanish question, snippet or answer.', null=True, verbose_name='Last edited Spanish content', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='next_step',
            field=models.ForeignKey(blank=True, to='ask_cfpb.NextStep', help_text='Also called action items or upsell items', null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question_es',
            field=models.TextField(verbose_name='Spanish question', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='slug_es',
            field=models.SlugField(max_length=255, verbose_name='Spanish slug', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='snippet_es',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Optional Spanish answer intro', verbose_name='Spanish snippet', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='subcategory',
            field=models.ManyToManyField(help_text='Choose any subcategories related to the answer', to='ask_cfpb.SubCategory', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='tagging',
            field=models.CharField(help_text='Search words or phrases, separated by commas', max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='update_english_page',
            field=models.BooleanField(default=False, verbose_name='Send to English page for review'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='update_spanish_page',
            field=models.BooleanField(default=False, verbose_name='Send to Spanish page for review'),
        ),
    ]

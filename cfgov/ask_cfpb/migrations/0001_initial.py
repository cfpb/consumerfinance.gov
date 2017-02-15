# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.db.models.deletion
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0057_add_reusable_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(blank=True)),
                ('snippet', wagtail.wagtailcore.fields.RichTextField(help_text='Optional answer intro', blank=True)),
                ('answer', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('question_es', models.TextField(blank=True)),
                ('snippet_es', wagtail.wagtailcore.fields.RichTextField(help_text='Optional Spanish answer intro', blank=True)),
                ('answer_es', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('slug_es', models.SlugField(max_length=255, blank=True)),
                ('tagging', models.CharField(help_text='Tags used for search index', max_length=1000, blank=True)),
                ('update_english_page', models.BooleanField(default=False, verbose_name='Update the English page when saving')),
                ('update_spanish_page', models.BooleanField(default=False, verbose_name='Update the Spanish page when saving')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_edited', models.DateField(help_text='Change the date to today if you edit an English question, snippet or answer.', null=True, blank=True)),
                ('last_edited_es', models.DateField(help_text='Change the date to today if you edit a Spanish question, snippet or answer.', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('question', wagtail.wagtailcore.fields.RichTextField(editable=False, blank=True)),
                ('answer', wagtail.wagtailcore.fields.RichTextField(editable=False, blank=True)),
                ('snippet', wagtail.wagtailcore.fields.RichTextField(help_text=b'Optional answer intro', editable=False, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('answer_base', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.Answer', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('name_es', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('slug_es', models.SlugField()),
                ('intro', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('intro_es', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('featured_questions', models.ManyToManyField(related_name='featured_questions', to='ask_cfpb.Answer', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='NextStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('show_title', models.BooleanField(default=False)),
                ('text', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('name_es', models.CharField(max_length=255, null=True, blank=True)),
                ('slug', models.SlugField()),
                ('slug_es', models.SlugField(null=True, blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('weight', models.IntegerField(default=1)),
                ('description', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('description_es', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('more_info', models.TextField(blank=True)),
                ('parent', models.ForeignKey(default=None, blank=True, to='ask_cfpb.Category', null=True)),
                ('related_subcategories', models.ManyToManyField(default=None, related_name='_subcategory_related_subcategories_+', to='ask_cfpb.SubCategory', blank=True)),
            ],
            options={
                'ordering': ['-weight'],
                'verbose_name_plural': 'Subcategories',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='audiences',
            field=models.ManyToManyField(to='ask_cfpb.Audience', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='category',
            field=models.ManyToManyField(to='ask_cfpb.Category', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='next_step',
            field=models.ForeignKey(blank=True, to='ask_cfpb.NextStep', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='related_questions',
            field=models.ManyToManyField(help_text='Maximum of 3', related_name='related_question', to='ask_cfpb.Answer', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='subcategory',
            field=models.ManyToManyField(to='ask_cfpb.SubCategory', blank=True),
        ),
    ]

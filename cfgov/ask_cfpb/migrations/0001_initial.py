# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import v1.util.filterable_list
import v1.feeds
import django.db.models.deletion
import v1.util.ref
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0066_fix_for_linking_video_stills'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='AnswerCategoryPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('content', wagtail.wagtailcore.fields.StreamField([('filter_controls', wagtail.wagtailcore.blocks.StructBlock([(b'label', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'is_bordered', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'is_midtone', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'is_expanded', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'form_type', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'filterable-list', choices=[(b'filterable-list', b'Filterable List'), (b'pdf-generator', b'PDF Generator')])), (b'title', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Filter Title')), (b'post_date_description', wagtail.wagtailcore.blocks.CharBlock(default=b'Published')), (b'categories', wagtail.wagtailcore.blocks.StructBlock([(b'filter_category', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False)), (b'show_preview_categories', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False)), (b'page_type', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=v1.util.ref.filterable_list_page_types))])), (b'topics', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Filter Topics')), (b'authors', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Filter Authors')), (b'date_range', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Filter Date Range')), (b'output_5050', wagtail.wagtailcore.blocks.BooleanBlock(default=False, required=False, label=b'Render preview items as 50-50s')), (b'link_image_and_heading', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Add links to post preview images and headings in filterable list results', default=False, required=False))]))], null=True)),
                ('secondary_nav_exclude_sibling_pages', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(v1.feeds.FilterableFeedPageMixin, v1.util.filterable_list.FilterableListMixin, 'v1.cfgovpage'),
        ),
        migrations.CreateModel(
            name='AnswerLandingPage',
            fields=[
                ('landingpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.LandingPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.landingpage',),
        ),
        migrations.CreateModel(
            name='AnswerPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('question', wagtail.wagtailcore.fields.RichTextField(editable=False, blank=True)),
                ('answer', wagtail.wagtailcore.fields.RichTextField(editable=False, blank=True)),
                ('snippet', wagtail.wagtailcore.fields.RichTextField(help_text='Optional answer intro', editable=False, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', wagtail.wagtailcore.fields.StreamField([('feedback', wagtail.wagtailcore.blocks.StructBlock([(b'was_it_helpful_text', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Use this field only for feedback forms that use "Was this helpful?" radio buttons.', default=b'Was this page helpful to you?', required=False)), (b'intro_text', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Optional feedback intro', required=False)), (b'question_text', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Optional expansion on intro', required=False)), (b'radio_intro', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Leave blank unless you are building a feedback form with extra radio-button prompts, as in /owning-a-home/help-us-improve/.', required=False)), (b'radio_text', wagtail.wagtailcore.blocks.CharBlock(default=b'This information helps us understand your question better.', required=False)), (b'radio_question_1', wagtail.wagtailcore.blocks.CharBlock(default=b'How soon do you expect to buy a home?', required=False)), (b'radio_question_2', wagtail.wagtailcore.blocks.CharBlock(default=b'Do you currently own a home?', required=False)), (b'button_text', wagtail.wagtailcore.blocks.CharBlock(default=b'Submit')), (b'contact_advisory', wagtail.wagtailcore.blocks.RichTextBlock(help_text=b'Use only for feedback forms that ask for a contact email', required=False))]))], blank=True)),
                ('answer_base', models.ForeignKey(related_name='answer_pages', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ask_cfpb.Answer', null=True)),
                ('redirect_to', models.ForeignKey(related_name='redirected_pages', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ask_cfpb.Answer', help_text='Choose another Answer to redirect this page to', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='AnswerResultsPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
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
                ('weight', models.IntegerField(default=1)),
                ('description', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('description_es', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('more_info', models.TextField(blank=True)),
                ('parent', models.ForeignKey(related_name='subcategories', default=None, blank=True, to='ask_cfpb.Category', null=True)),
                ('related_subcategories', models.ManyToManyField(default=None, related_name='_subcategory_related_subcategories_+', to='ask_cfpb.SubCategory', blank=True)),
            ],
            options={
                'ordering': ['weight'],
                'verbose_name_plural': 'Subcategories',
            },
        ),
        migrations.AddField(
            model_name='answercategorypage',
            name='ask_category',
            field=models.ForeignKey(related_name='category_page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.Category', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='audiences',
            field=models.ManyToManyField(help_text='Pick any audiences that may be interested in the answer', to='ask_cfpb.Audience', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='category',
            field=models.ManyToManyField(help_text='This associates an answer with a portal page', to='ask_cfpb.Category', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='last_user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='next_step',
            field=models.ForeignKey(blank=True, to='ask_cfpb.NextStep', help_text='Also called action items or upsell items', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='related_questions',
            field=models.ManyToManyField(help_text='Maximum of 3', related_name='related_question', to='ask_cfpb.Answer', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='subcategory',
            field=models.ManyToManyField(help_text='Choose any subcategories related to the answer', to='ask_cfpb.SubCategory', blank=True),
        ),
        migrations.CreateModel(
            name='EnglishAnswerProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('ask_cfpb.answer',),
        ),
        migrations.CreateModel(
            name='SpanishAnswerProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('ask_cfpb.answer',),
        ),
    ]

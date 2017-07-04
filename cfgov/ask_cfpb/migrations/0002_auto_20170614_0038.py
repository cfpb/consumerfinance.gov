# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.contrib.wagtailroutablepage.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ask_cfpb', '0001_initial'),
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerAudiencePage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('content', wagtail.wagtailcore.fields.StreamField([], null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.CreateModel(
            name='AnswerCategoryPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('content', wagtail.wagtailcore.fields.StreamField([], null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'v1.cfgovpage'),
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
                ('content', wagtail.wagtailcore.fields.StreamField([], null=True)),
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
                ('category_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text='Select a custom image to appear when visitors share pages belonging to this category on social media.', null=True)),
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
        migrations.CreateModel(
            name='TagResultsPage',
            fields=[
                ('answerresultspage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ask_cfpb.AnswerResultsPage')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'ask_cfpb.answerresultspage'),
        ),
        migrations.AddField(
            model_name='answercategorypage',
            name='ask_category',
            field=models.ForeignKey(related_name='category_page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.Category', null=True),
        ),
        migrations.AddField(
            model_name='answercategorypage',
            name='ask_subcategory',
            field=models.ForeignKey(related_name='subcategory_page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.SubCategory', null=True),
        ),
        migrations.AddField(
            model_name='answeraudiencepage',
            name='ask_audience',
            field=models.ForeignKey(related_name='audience_page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.Audience', null=True),
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
            name='social_sharing_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text="Optionally select a custom image to appear when users share this page on social media websites. If no image is selected, this page's category image will be used.", null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='subcategory',
            field=models.ManyToManyField(help_text='Choose any subcategories related to the answer', to='ask_cfpb.SubCategory', blank=True),
        ),
        migrations.CreateModel(
            name='AnswerTagProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('ask_cfpb.answer',),
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

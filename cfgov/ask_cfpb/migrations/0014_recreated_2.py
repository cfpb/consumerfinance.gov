# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailsnippets.blocks
import v1.models.snippets
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import ask_cfpb.models.pages
import wagtail.contrib.wagtailroutablepage.models
import django.utils.timezone
import django.db.models.deletion
from django.conf import settings
import v1.blocks


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
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ask_cfpb', '0013_recreated'),
        ('v1', '0102_recreated'),
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
            bases=(ask_cfpb.models.pages.SecondaryNavigationJSMixin, 'v1.cfgovpage'),
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
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, ask_cfpb.models.pages.SecondaryNavigationJSMixin, 'v1.cfgovpage'),
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
                ('sidebar', wagtail.wagtailcore.fields.StreamField([('call_to_action', wagtail.wagtailcore.blocks.StructBlock([(b'slug_text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph_text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'button', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False)), (b'size', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'regular', b'Regular'), (b'large', b'Large Primary')]))]))])), ('related_links', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])))])), ('related_metadata', wagtail.wagtailcore.blocks.StructBlock([(b'slug', wagtail.wagtailcore.blocks.CharBlock(max_length=100)), (b'content', wagtail.wagtailcore.blocks.StreamBlock([(b'text', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100)), (b'blob', wagtail.wagtailcore.blocks.RichTextBlock())], icon=b'pilcrow')), (b'list', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])))], icon=b'list-ul')), (b'date', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100)), (b'date', wagtail.wagtailcore.blocks.DateBlock())], icon=b'date')), (b'topics', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(default=b'Topics', max_length=100)), (b'show_topics', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False))], icon=b'tag'))])), (b'is_half_width', wagtail.wagtailcore.blocks.BooleanBlock(default=False, required=False))])), ('email_signup', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'gd_code', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'form_field', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'btn_text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'required', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'info', wagtail.wagtailcore.blocks.RichTextBlock(required=False, label=b'Disclaimer')), (b'label', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'type', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=[(b'text', b'Text'), (b'checkbox', b'Checkbox'), (b'email', b'Email'), (b'number', b'Number'), (b'url', b'URL'), (b'radio', b'Radio')])), (b'placeholder', wagtail.wagtailcore.blocks.CharBlock(required=False))]), required=False, icon=b'mail'))])), ('sidebar_contact', wagtail.wagtailcore.blocks.StructBlock([(b'contact', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(b'v1.Contact')), (b'has_top_rule_line', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Add a horizontal rule line to top of contact block.', default=False, required=False))])), ('rss_feed', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[(b'blog_feed', b'Blog Feed'), (b'newsroom_feed', b'Newsroom Feed')])), ('social_media', wagtail.wagtailcore.blocks.StructBlock([(b'is_share_view', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'If unchecked, social media icons will link users to official CFPB accounts. Do not fill in any further fields.', default=True, required=False, label=b'Desired action: share this page')), (b'blurb', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Sets the tweet text, email subject line, and LinkedIn post text.', default=b"Look what I found on the CFPB's site!", required=False)), (b'twitter_text', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) Custom text for Twitter shares. If blank, will default to value of blurb field above.', max_length=100, required=False)), (b'twitter_related', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) A comma-separated list of accounts related to the content of the shared URL. Do not enter the  @ symbol. If blank, it will default to just "cfpb".', required=False)), (b'twitter_hashtags', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) A comma-separated list of hashtags to be appended to default tweet text.', required=False)), (b'twitter_lang', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) Loads text components in the specified language, if other than English. E.g., use "es"  for Spanish. See https://dev.twitter.com/web/overview/languages for a list of supported language codes.', required=False)), (b'email_title', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) Custom subject for email shares. If blank, will default to value of blurb field above.', required=False)), (b'email_text', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) Custom text for email shares. If blank, will default to "Check out this page from the CFPB".', required=False)), (b'email_signature', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) Adds a custom signature line to email shares. ', required=False)), (b'linkedin_title', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) Custom title for LinkedIn shares. If blank, will default to value of blurb field above.', required=False)), (b'linkedin_text', wagtail.wagtailcore.blocks.CharBlock(help_text=b'(Optional) Custom text for LinkedIn shares.', required=False))])), ('reusable_text', v1.blocks.ReusableTextChooserBlock(v1.models.snippets.ReusableText))], blank=True)),
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
            bases=(ask_cfpb.models.pages.SecondaryNavigationJSMixin, 'v1.cfgovpage'),
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
                ('slug', models.SlugField(help_text='Do not edit this field')),
                ('slug_es', models.SlugField(help_text='Do not edit this field')),
                ('intro', wagtail.wagtailcore.fields.RichTextField(help_text='Do not use H2, H3, H4, or H5 to style this text. Do not add links, images, videos or other rich text elements.', blank=True)),
                ('intro_es', wagtail.wagtailcore.fields.RichTextField(help_text='Do not use this field. It is not currently displayed on the front end.', blank=True)),
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
                ('slug_es', models.SlugField(help_text='This field is not currently used on the front end.', null=True, blank=True)),
                ('weight', models.IntegerField(default=1)),
                ('description', wagtail.wagtailcore.fields.RichTextField(help_text='This field is not currently displayed on the front end.', blank=True)),
                ('description_es', wagtail.wagtailcore.fields.RichTextField(help_text='This field is not currently displayed on the front end.', blank=True)),
                ('more_info', models.TextField(help_text='This field is not currently displayed on the front end.', blank=True)),
                ('parent', models.ForeignKey(related_name='subcategories', default=None, blank=True, to='ask_cfpb.Category', null=True)),
                ('related_subcategories', models.ManyToManyField(default=None, help_text='Maximum 3 related subcategories', related_name='_subcategory_related_subcategories_+', to='ask_cfpb.SubCategory', blank=True)),
            ],
            options={
                'ordering': ['weight'],
                'verbose_name_plural': 'subcategories',
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
            field=models.ManyToManyField(help_text='Tag any audiences that may be interested in the answer.', to='ask_cfpb.Audience', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='category',
            field=models.ManyToManyField(help_text='Categorize this answer. Avoid putting into more than one category.', to='ask_cfpb.Category', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='last_user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='next_step',
            field=models.ForeignKey(blank=True, to='ask_cfpb.NextStep', help_text="Formerly known as action items or upsell items.On the web page, these are labeled as 'Explore related resources.'", null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='related_questions',
            field=models.ManyToManyField(help_text='Maximum of 3', related_name='related_question', to='ask_cfpb.Answer', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='social_sharing_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', help_text="Optionally select a custom image to appear when users share this page on social media websites. If no image is selected, this page's category image will be used. Minimum size: 1200w x 630h.", null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='subcategory',
            field=models.ManyToManyField(help_text='Choose only subcategories that belong to one of the categories checked above.', to='ask_cfpb.SubCategory', blank=True),
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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailsnippets.blocks
import v1.models.snippets
import modelcluster.contrib.taggit
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
        ('taggit', '0002_auto_20150616_2121'),
        ('v1', '0039_remove_blog_from_category_choice'),
    ]

    operations = [
        migrations.CreateModel(
            name='CFGOVFormPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('shared', models.BooleanField(default=False)),
                ('language', models.CharField(default=b'en', max_length=2, choices=[(b'en', b'English'), (b'es', b'Spanish'), (b'zh', b'Chinese'), (b'vi', b'Vietnamese'), (b'ko', b'Korean'), (b'tl', b'Tagalog'), (b'ru', b'Russian'), (b'ar', b'Arabic'), (b'ht', b'Haitian Creole')])),
                ('sidefoot', wagtail.wagtailcore.fields.StreamField([(b'slug', wagtail.wagtailcore.blocks.CharBlock(icon=b'title')), (b'heading', wagtail.wagtailcore.blocks.CharBlock(icon=b'title')), (b'paragraph', wagtail.wagtailcore.blocks.TextBlock(icon=b'edit')), (b'hyperlink', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])), (b'call_to_action', wagtail.wagtailcore.blocks.StructBlock([(b'slug_text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'paragraph_text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'button', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))])), (b'related_links', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])))])), (b'related_posts', wagtail.wagtailcore.blocks.StructBlock([(b'limit', wagtail.wagtailcore.blocks.CharBlock(default=b'3', label=b'Limit')), (b'show_heading', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'This toggles the heading and icon for the related types.', default=True, required=False, label=b'Show Heading and Icon?')), (b'relate_posts', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, editable=False, label=b'Blog Posts')), (b'relate_newsroom', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, editable=False, label=b'Newsroom')), (b'relate_events', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Events')), (b'view_more', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))])), (b'email_signup', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'gd_code', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'form_field', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'btn_text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'required', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'id', wagtail.wagtailcore.blocks.CharBlock(help_text=b'Type of form i.e emailForm, submission-form. Should be unique if multiple forms are used', max_length=100, required=False)), (b'info', wagtail.wagtailcore.blocks.RichTextBlock(required=False, label=b'Disclaimer')), (b'label', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=True)), (b'type', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=[(b'text', b'Text'), (b'checkbox', b'Checkbox'), (b'email', b'Email'), (b'number', b'Number'), (b'url', b'URL'), (b'radio', b'Radio')])), (b'placeholder', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False))]), required=False, icon=b'mail'))])), (b'contact', wagtail.wagtailcore.blocks.StructBlock([(b'header', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'contact', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(v1.models.snippets.Contact))]))], blank=True)),
                ('authors', modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='v1.CFGOVAuthoredPages', blank=True, help_text=b'A comma separated list of authors.', verbose_name=b'Authors')),
                ('tags', modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='v1.CFGOVTaggedPages', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.RemoveField(
            model_name='documentdetailpage',
            name='abstractfilterpage_ptr',
        ),
        migrations.RemoveField(
            model_name='eventpage',
            name='abstractfilterpage_ptr',
        ),
        migrations.RemoveField(
            model_name='learnpage',
            name='abstractfilterpage_ptr',
        ),
        migrations.RemoveField(
            model_name='abstractfilterpage',
            name='cfgovpage_ptr',
        ),
        migrations.AddField(
            model_name='abstractfilterpage',
            name='cfgovformpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVFormPage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentdetailpage',
            name='abstractfilterpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.AbstractFilterPage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpage',
            name='abstractfilterpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.AbstractFilterPage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='learnpage',
            name='abstractfilterpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.AbstractFilterPage'),
            preserve_default=False,
        ),
    ]

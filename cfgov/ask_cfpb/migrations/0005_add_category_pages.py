# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import django.db.models.deletion
import v1.util.ref
import v1.feeds
import wagtail.wagtailcore.blocks
import v1.util.filterable_list


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0060_feedback_language'),
        ('ask_cfpb', '0004_answerpage_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerCategoryPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('content', wagtail.wagtailcore.fields.StreamField([('filter_controls', wagtail.wagtailcore.blocks.StructBlock([(b'label', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'is_bordered', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'is_midtone', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'is_expanded', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'form_type', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'filterable-list', choices=[(b'filterable-list', b'Filterable List'), (b'pdf-generator', b'PDF Generator')])), (b'title', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Filter Title')), (b'post_date_description', wagtail.wagtailcore.blocks.CharBlock(default=b'Published')), (b'categories', wagtail.wagtailcore.blocks.StructBlock([(b'filter_category', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False)), (b'show_preview_categories', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False)), (b'page_type', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=v1.util.ref.filterable_list_page_types))])), (b'topics', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Filter Topics')), (b'authors', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Filter Authors')), (b'date_range', wagtail.wagtailcore.blocks.BooleanBlock(default=True, required=False, label=b'Filter Date Range')), (b'output_5050', wagtail.wagtailcore.blocks.BooleanBlock(default=False, required=False, label=b'Render preview items as 50-50s')), (b'should_link_image', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Add links to post preview images in filterable list results', default=False, required=False))]))], null=True)),
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
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ['weight'], 'verbose_name_plural': 'Subcategories'},
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='tagging',
            new_name='search_tags',
        ),
        migrations.RemoveField(
            model_name='category',
            name='featured_questions',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='featured',
        ),
        migrations.AddField(
            model_name='answer',
            name='featured',
            field=models.BooleanField(default=False, help_text='Makes the answer available to cards on the landing page'),
        ),
        migrations.AddField(
            model_name='answer',
            name='featured_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='parent',
            field=models.ForeignKey(related_name='subcategories', default=None, blank=True, to='ask_cfpb.Category', null=True),
        ),
        migrations.AddField(
            model_name='answercategorypage',
            name='ask_category',
            field=models.ForeignKey(related_name='category_page', on_delete=django.db.models.deletion.PROTECT, blank=True, to='ask_cfpb.Category', null=True),
        ),
    ]

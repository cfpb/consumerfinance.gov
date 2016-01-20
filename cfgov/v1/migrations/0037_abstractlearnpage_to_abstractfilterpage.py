# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import wagtail.wagtailcore.fields
import django.db.models.deletion
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('v1', '0036_move_events_into_learn'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractFilterPage',
            fields=[
                ('cfgovpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='v1.CFGOVPage')),
                ('header', wagtail.wagtailcore.fields.StreamField([(b'text_introduction', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(required=False))])), (b'item_introduction', wagtail.wagtailcore.blocks.StructBlock([(b'category', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=[(b'Amicus Brief', ((b'us-supreme-court', b'U.S. Supreme Court'), (b'fed-circuit-court', b'Federal Circuit Court'), (b'fed-district-court', b'Federal District Court'), (b'state-court', b'State Court'))), (b'Blog', ((b'at-the-cfpb', b'At the CFPB'), (b'cfpb_report', b'CFPB Report'), (b'data-research-reports', b'Data, research & reports'), (b'info-for-consumers', b'Info for consumers'))), (b'Enforcement action', ((b'fed-district-case', b'Federal District Court Case'), (b'admin-adj-process', b'Administrative Adjudication Process'))), (b'Final Rule', ((b'interim-final-rule', b'Interim Final Rule'), (b'final-rule', b'Final Rule'))), (b'FOIA Frequently Requested Record', ((b'report', b'Report'), (b'log', b'Log'), (b'record', b'Record'))), (b'Implementation Resource', ((b'cfpb-bulletins-statements', b'CFPB Bulletins and Statements'), (b'impl-compl-material', b'Implementation and Compliance Material'))), (b'Newsroom', ((b'blog', b'Blog'), (b'op-ed', b'Op-Ed'), (b'press-release', b'Press Release'), (b'speech', b'Speech'), (b'testimony', b'Testimony'))), (b'Notice and Opportunity for Comment', ((b'notice-proposed-rule', b'Advanced Notice of Proposed Rulemaking'), (b'proposed-rule', b'Proposed Rule'), (b'interim-final-rule-2', b'Interim Final Rule'), (b'request-comment-info', b'Request for Comment or Information'), (b'proposed-policy', b'Proposed Policy'), (b'intent-preempt-determ', b'Intent to make Preemption Determination'), (b'info-collect-activity', b'Information Collection Activities'), (b'notice-privacy-act', b'Notice related to Privacy Act'))), (b'Research Report', ((b'consumer-complaint', b'Consumer Complaint'), (b'super-highlight', b'Supervisory Highlights'), (b'data-point', b'Data Point'), (b'snapshot', b'Snapshot'), (b'consumer-voices', b'Consumer Voices'), (b'education-programs', b'Education and Programs'), (b'our-regulations', b'Our Regulations'), (b'industry-practices', b'Industry Practices'), (b'joint-reports', b'Joint Reports'), (b'finances-results', b'Finances and Results'))), (b'Rule under development', ((b'notice-proposed-rule-2', b'Advanced Notice of Proposed Rulemaking'), (b'proposed-rule-2', b'Proposed Rule')))])), (b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'authors', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))), (b'date', wagtail.wagtailcore.blocks.DateTimeBlock(required=False)), (b'has_social', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Whether to show the share icons or not.', required=False))]))], blank=True)),
                ('preview_title', models.CharField(max_length=255, null=True, blank=True)),
                ('preview_subheading', models.CharField(max_length=255, null=True, blank=True)),
                ('preview_description', wagtail.wagtailcore.fields.RichTextField(null=True, blank=True)),
                ('preview_link_text', models.CharField(max_length=255, null=True, blank=True)),
                ('date_published', models.DateField(default=datetime.datetime.now)),
                ('date_filed', models.DateField(null=True, blank=True)),
                ('comments_close_by', models.DateField(null=True, blank=True)),
                ('preview_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='v1.CFGOVImage', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('v1.cfgovpage',),
        ),
        migrations.RemoveField(
            model_name='documentdetailpage',
            name='abstractlearnpage_ptr',
        ),
        migrations.RemoveField(
            model_name='eventpage',
            name='abstractlearnpage_ptr',
        ),
        migrations.RemoveField(
            model_name='learnpage',
            name='abstractlearnpage_ptr',
        ),
        migrations.DeleteModel(
            name='AbstractLearnPage',
        ),
        migrations.AddField(
            model_name='documentdetailpage',
            name='abstractfilterpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=4L, serialize=False, to='v1.AbstractFilterPage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpage',
            name='abstractfilterpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=5L, serialize=False, to='v1.AbstractFilterPage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='learnpage',
            name='abstractfilterpage_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=4L, serialize=False, to='v1.AbstractFilterPage'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import pytz
import datetime
from dateutil import parser

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks


def convert_datetimes(apps, schema_editor):
    HomePage = apps.get_model('v1.HomePage')
    DemoPage = apps.get_model('v1.DemoPage')
    Page = apps.get_model('wagtailcore.Page')
    PageRevision = apps.get_model('wagtailcore.PageRevision')

    def specific(page):
        content_type = ContentType.objects.get_for_id(page.content_type_id)
        model_class = content_type.model_class()
        if model_class is None:
            return page
        elif isinstance(page, model_class):
            return page
        else:
            return content_type.get_object_for_this_type(id=page.id)

    local = pytz.timezone('America/New_York')
    def timezone_conversion(dt):
        if isinstance(dt, basestring):
            dt = parser.parse(dt)
        naive = dt.replace(tzinfo=None)
        localized_dt = local.localize(naive)
        return localized_dt.astimezone(pytz.utc)

    home = HomePage.objects.filter(slug='cfgov').first()
    if home:
        for update in home.latest_updates:
            if update.block_type == 'posts':
                for post in update.value:
                    post['date'] = timezone_conversion(post['date'])
        home.save()
        revision = PageRevision.objects.filter(page=home).order_by('-id').first()
        content = json.loads(revision.content_json)
        if 'latest_updates' in content:
            latest_updates = json.loads(content['latest_updates'])
            for i, update in enumerate(latest_updates):
                for j, value in enumerate(update['value']):
                    if value['date']:
                        latest_updates[i]['value'][j]['date'] = timezone_conversion(value['date']).isoformat()
            content['latest_updates'] = json.dumps(latest_updates)
            revision.content_json = json.dumps(content)
        revision.save()

    if settings.DEBUG:
        for demo in DemoPage.objects.all():
            for block in demo.organisms:
                if block.block_type == 'item_intro':
                    datetime = block.value['date']
                    if datetime:
                        block.value['date'] = datetime.date()
            demo.save()

    for page in Page.objects.all():
        if page.go_live_at:
            page.go_live_at = timezone_conversion(page.go_live_at)
            for revision in PageRevision.objects.filter(page=page).order_by('-id'):
                revision.approved_go_live_at = page.go_live_at
                revision.save()
        if page.expire_at:
            page.expire_at = timezone_conversion(page.expire_at)
        page.save()
        specific_page = specific(page)
        if 'learn_page' in str(type(specific_page)):
            for block in specific_page.header:
                if block.block_type == 'item_introduction':
                    datetime = block.value['date']
                    if datetime:
                        block.value['date'] = datetime.date()
            specific_page.save()
            revision = PageRevision.objects.filter(page=page).order_by('-id').first()
            content = json.loads(revision.content_json)
            if 'header' in content:
                header = json.loads(content['header'])
                for i, block in enumerate(header):
                    if block['type'] == 'item_introduction':
                        if block['value']['date']:
                            header[i]['value']['date'] = timezone_conversion(block['value']['date']).date().isoformat()
                content['header'] = json.dumps(header)
                revision.content_json = json.dumps(content)
            revision.save()
        if 'EventPage' in str(type(specific_page)):
            if specific_page.start_dt:
                specific_page.start_dt = timezone_conversion(specific_page.start_dt)
            if specific_page.end_dt:
                specific_page.end_dt = timezone_conversion(specific_page.end_dt)
            if specific_page.live_stream_date:
                specific_page.live_stream_date = timezone_conversion(specific_page.live_stream_date)
            for item in specific_page.agenda_items:
                if item.block_type == 'item':
                    for old, new in {'start_dt': 'start_time', 'end_dt': 'end_time'}.iteritems():
                        if old in item.value and item.value[old]:
                            item.value[new] = item.value[old].time()
                            del item.value[old]
            specific_page.save()
            revision = PageRevision.objects.filter(page=page).order_by('-id').first()
            content = json.loads(revision.content_json)
            for time in ['start_dt', 'end_dt', 'live_stream_date']:
                if time in content and content[time]:
                    content[time] = timezone_conversion(content[time]).isoformat()
            if 'agenda_items' in content:
                agenda_items = json.loads(content['agenda_items'])
                for i, item in enumerate(agenda_items):
                    if item['type'] == 'item':
                        for old, new in {'start_dt': 'start_time', 'end_dt': 'end_time'}.iteritems():
                            if old in item['value'] and item['value'][old]:
                                agenda_items[i]['value'][new] = parser.parse(item['value'][old]).time().isoformat()
                                del agenda_items[i]['value'][old]
                content['agenda_items'] = json.dumps(agenda_items)
            revision.content_json = json.dumps(content)
            revision.save()


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0089_auto_20160607_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractfilterpage',
            name='header',
            field=wagtail.wagtailcore.fields.StreamField([(b'article_subheader', wagtail.wagtailcore.blocks.RichTextBlock(icon=b'form')), (b'text_introduction', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'intro', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]), required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(required=False))])), (b'item_introduction', wagtail.wagtailcore.blocks.StructBlock([(b'category', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=[(b'Amicus Brief', ((b'us-supreme-court', b'U.S. Supreme Court'), (b'fed-circuit-court', b'Federal Circuit Court'), (b'fed-district-court', b'Federal District Court'), (b'state-court', b'State Court'))), (b'Blog', ((b'at-the-cfpb', b'At the CFPB'), (b'policy_compliance', b'Policy & Compliance'), (b'data-research-reports', b'Data, research & reports'), (b'info-for-consumers', b'Info for consumers'))), (b'Enforcement action', ((b'fed-district-case', b'Federal District Court Case'), (b'admin-filing', b'Administrative Filing'))), (b'Final Rule', ((b'interim-final-rule', b'Interim Final Rule'), (b'final-rule', b'Final Rule'))), (b'FOIA Frequently Requested Record', ((b'report', b'Report'), (b'log', b'Log'), (b'record', b'Record'))), (b'Implementation Resource', ((b'compliance-aid', b'Compliance aid'), (b'official-guidance', b'Official guidance'))), (b'Newsroom', ((b'op-ed', b'Op-Ed'), (b'press-release', b'Press Release'), (b'speech', b'Speech'), (b'testimony', b'Testimony'))), (b'Notice and Opportunity for Comment', ((b'notice-proposed-rule', b'Advanced Notice of Proposed Rulemaking'), (b'proposed-rule', b'Proposed Rule'), (b'interim-final-rule-2', b'Interim Final Rule'), (b'request-comment-info', b'Request for Comment or Information'), (b'proposed-policy', b'Proposed Policy'), (b'intent-preempt-determ', b'Intent to make Preemption Determination'), (b'info-collect-activity', b'Information Collection Activities'), (b'notice-privacy-act', b'Notice related to Privacy Act'))), (b'Research Report', ((b'consumer-complaint', b'Consumer Complaint'), (b'super-highlight', b'Supervisory Highlights'), (b'data-point', b'Data Point'), (b'industry-markets', b'Industry and markets'), (b'consumer-edu-empower', b'Consumer education and empowerment'), (b'to-congress', b'To Congress'))), (b'Rule under development', ((b'notice-proposed-rule-2', b'Advanced Notice of Proposed Rulemaking'), (b'proposed-rule-2', b'Proposed Rule')))])), (b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'date', wagtail.wagtailcore.blocks.DateBlock(required=False)), (b'has_social', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Whether to show the share icons or not.', required=False))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='demopage',
            name='organisms',
            field=wagtail.wagtailcore.fields.StreamField([(b'well', wagtail.wagtailcore.blocks.StructBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(required=False, label=b'Well'))])), (b'full_width_text', wagtail.wagtailcore.blocks.StreamBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(icon=b'edit')), (b'media', wagtail.wagtailimages.blocks.ImageChooserBlock(icon=b'image')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'body', wagtail.wagtailcore.blocks.TextBlock()), (b'citation', wagtail.wagtailcore.blocks.TextBlock())])), (b'cta', wagtail.wagtailcore.blocks.StructBlock([(b'slug_text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph_text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'button', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))]))])), (b'related_links', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'links', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])))])), (b'table', wagtail.wagtailcore.blocks.StructBlock([(b'headers', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.CharBlock())), (b'rows', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StreamBlock([(b'hyperlink', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])), (b'text', wagtail.wagtailcore.blocks.CharBlock()), (b'text_blob', wagtail.wagtailcore.blocks.TextBlock()), (b'rich_text_blob', wagtail.wagtailcore.blocks.RichTextBlock())])))]))])), (b'expandable_group', wagtail.wagtailcore.blocks.StructBlock([(b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'body', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'is_accordion', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'has_rule', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'expandables', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'label', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'is_bordered', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'is_midtone', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'is_expanded', wagtail.wagtailcore.blocks.BooleanBlock(required=False)), (b'content', wagtail.wagtailcore.blocks.StreamBlock([(b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'well', wagtail.wagtailcore.blocks.StructBlock([(b'content', wagtail.wagtailcore.blocks.RichTextBlock(required=False, label=b'Well'))])), (b'links', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])), (b'email', wagtail.wagtailcore.blocks.StructBlock([(b'emails', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.CharBlock(default=b'/', required=False))])))])), (b'phone', wagtail.wagtailcore.blocks.StructBlock([(b'fax', wagtail.wagtailcore.blocks.BooleanBlock(default=False, required=False, label=b'Is this number a fax?')), (b'phones', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'number', wagtail.wagtailcore.blocks.CharBlock(max_length=15)), (b'vanity', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False)), (b'tty', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False))])))])), (b'address', wagtail.wagtailcore.blocks.StructBlock([(b'label', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'street', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'city', wagtail.wagtailcore.blocks.CharBlock(max_length=50, required=False)), (b'state', wagtail.wagtailcore.blocks.CharBlock(max_length=25, required=False)), (b'zip_code', wagtail.wagtailcore.blocks.CharBlock(max_length=15, required=False))]))], blank=True))])))])), (b'item_intro', wagtail.wagtailcore.blocks.StructBlock([(b'category', wagtail.wagtailcore.blocks.ChoiceBlock(required=False, choices=[(b'Amicus Brief', ((b'us-supreme-court', b'U.S. Supreme Court'), (b'fed-circuit-court', b'Federal Circuit Court'), (b'fed-district-court', b'Federal District Court'), (b'state-court', b'State Court'))), (b'Blog', ((b'at-the-cfpb', b'At the CFPB'), (b'policy_compliance', b'Policy & Compliance'), (b'data-research-reports', b'Data, research & reports'), (b'info-for-consumers', b'Info for consumers'))), (b'Enforcement action', ((b'fed-district-case', b'Federal District Court Case'), (b'admin-filing', b'Administrative Filing'))), (b'Final Rule', ((b'interim-final-rule', b'Interim Final Rule'), (b'final-rule', b'Final Rule'))), (b'FOIA Frequently Requested Record', ((b'report', b'Report'), (b'log', b'Log'), (b'record', b'Record'))), (b'Implementation Resource', ((b'compliance-aid', b'Compliance aid'), (b'official-guidance', b'Official guidance'))), (b'Newsroom', ((b'op-ed', b'Op-Ed'), (b'press-release', b'Press Release'), (b'speech', b'Speech'), (b'testimony', b'Testimony'))), (b'Notice and Opportunity for Comment', ((b'notice-proposed-rule', b'Advanced Notice of Proposed Rulemaking'), (b'proposed-rule', b'Proposed Rule'), (b'interim-final-rule-2', b'Interim Final Rule'), (b'request-comment-info', b'Request for Comment or Information'), (b'proposed-policy', b'Proposed Policy'), (b'intent-preempt-determ', b'Intent to make Preemption Determination'), (b'info-collect-activity', b'Information Collection Activities'), (b'notice-privacy-act', b'Notice related to Privacy Act'))), (b'Research Report', ((b'consumer-complaint', b'Consumer Complaint'), (b'super-highlight', b'Supervisory Highlights'), (b'data-point', b'Data Point'), (b'industry-markets', b'Industry and markets'), (b'consumer-edu-empower', b'Consumer education and empowerment'), (b'to-congress', b'To Congress'))), (b'Rule under development', ((b'notice-proposed-rule-2', b'Advanced Notice of Proposed Rulemaking'), (b'proposed-rule-2', b'Proposed Rule')))])), (b'heading', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), (b'date', wagtail.wagtailcore.blocks.DateBlock(required=False)), (b'has_social', wagtail.wagtailcore.blocks.BooleanBlock(help_text=b'Whether to show the share icons or not.', required=False))]))], blank=True),
        ),
        migrations.RunPython(convert_datetimes),
        migrations.AlterField(
            model_name='eventpage',
            name='agenda_items',
            field=wagtail.wagtailcore.fields.StreamField([(b'item', wagtail.wagtailcore.blocks.StructBlock([(b'start_time', wagtail.wagtailcore.blocks.TimeBlock(required=False, label=b'Start')), (b'end_time', wagtail.wagtailcore.blocks.TimeBlock(required=False, label=b'End')), (b'description', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'location', wagtail.wagtailcore.blocks.CharBlock(max_length=100, required=False)), (b'speakers', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'name', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'url', wagtail.wagtailcore.blocks.URLBlock(required=False))], required=False, icon=b'user')))]))], blank=True),
        ),
    ]

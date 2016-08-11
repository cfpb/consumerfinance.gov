# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import v1.models.snippets
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailsnippets.blocks
import wagtail.wagtailimages.blocks
from wagtail.wagtailcore.models import Site
from django.conf import settings
from v1.models.learn_page import LearnPage, DocumentDetailPage
from v1.models.sublanding_page import SublandingPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.blog_page import BlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.demo import DemoPage
from v1.tests.wagtail_pages.helpers import publish_changes
from v1.models.base import CFGOVPage
from itertools import chain

def update_content_tables(wagtail_page):
    for item in wagtail_page.content.stream_data:
        if item['type'] == 'table':
            item['type'] = 'table_block'
            item['value'] = create_tableblock_data(old_table=item['value'])
            print "Creating a new TableBlock on page %s" %(wagtail_page.title)


def update_full_width_text_tables(wagtail_page):
    for item in wagtail_page.content.stream_data:
        if item['type'] == 'full_width_text':
            for sub_item in item['value']:
                if sub_item['type'] == 'table':
                    sub_item['type'] = 'table_block'
                    sub_item['value'] = create_tableblock_data(old_table=sub_item['value'])
                    print "Creating a new TableBlock on page %s" %(wagtail_page.title)


def create_tableblock_data(old_table):
    table = {u'data': []}
    if 'headers' in old_table.keys():
        first_row = old_table['headers']
        table['data'].append(first_row)
        table['first_row_is_table_header'] = True
    if 'rows' in old_table.keys():
        for row_list in old_table['rows']:
            new_row = []
            for row in row_list:
                new_row.append(row['value'])
            table['data'].append(new_row)
    return table


def create_tableblocks_for_every_table(apps,schema_editor):
    for p in chain(
        BrowsePage.objects.all(), 
        SublandingPage.objects.all(), 
        LearnPage.objects.all(),
        DocumentDetailPage.objects.all(),
    ):
        update_content_tables(wagtail_page=p)
        publish_changes(child=p)

    for p in chain(
        BlogPage.objects.all(),
        BrowseFilterablePage.objects.all(),
        BrowsePage.objects.all(),
        DemoPage.objects.all(),
        LearnPage.objects.all(),
        SublandingFilterablePage.objects.all(),
        SublandingPage.objects.all(),
    ):
        update_full_width_text_tables(wagtail_page=p)
        publish_changes(child=p)



class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0005_auto_20160811_1753'),
    ]

    operations = [
        migrations.RunPython(create_tableblocks_for_every_table)
    ]

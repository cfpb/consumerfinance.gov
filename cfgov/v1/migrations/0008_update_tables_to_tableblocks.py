# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from itertools import chain

from django.db import migrations

from v1.models.learn_page import LearnPage, DocumentDetailPage
from v1.models.sublanding_page import SublandingPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.blog_page import BlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.demo import DemoPage
from v1.tests.wagtail_pages.helpers import publish_changes


def update_table_items(items, wagtail_page):
    for item in list(filter(
        lambda item: item['type'] == 'table',
        items
    )):
        item['type'] = 'table_block'
        item['value'] = create_tableblock_data(old_table=item['value'])
        print(
            "Updating Table to a TableBlock on page %s of page type %s"
            % (wagtail_page.title, wagtail_page.__class__.__name__)
        )


def update_tables_in_content_field(wagtail_page):
    update_table_items(
        items=wagtail_page.content.stream_data,
        wagtail_page=wagtail_page
    )


def update_tables_in_full_width_text_organisms(wagtail_page):
    for item in list(filter(
            lambda item: item['type'] == 'full_width_text',
            wagtail_page.content.stream_data
    )):
        sub_items = item['value']
        update_table_items(items=sub_items, wagtail_page=wagtail_page)


def convert_hyperlink_obj_to_text(value):
    """ Taken from cfgov/jinja2/v1/_includes/atoms/hyperlink.html """
    return """<a class='jump-link' href='%s'>%s</a>""" % (
        value['url'],
        value['text']
    )


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
                if row['type'] == 'hyperlink':
                    row['value'] = convert_hyperlink_obj_to_text(row['value'])
                new_row.append(row['value'])
            table['data'].append(new_row)
    return table


def create_tableblocks_for_every_table(apps, schema_editor):
    print("Updating tables in content field")
    for p in chain(
        BrowsePage.objects.all(),
        SublandingPage.objects.all(),
        LearnPage.objects.all(),
        DocumentDetailPage.objects.all(),
    ):
        update_tables_in_content_field(wagtail_page=p)
        publish_changes(child=p)

    print("Updating tables in full width text organisms")
    for p in chain(
        BlogPage.objects.all(),
        BrowseFilterablePage.objects.all(),
        BrowsePage.objects.all(),
        DemoPage.objects.all(),
        LearnPage.objects.all(),
        SublandingFilterablePage.objects.all(),
        SublandingPage.objects.all(),
    ):
        update_tables_in_full_width_text_organisms(wagtail_page=p)
        publish_changes(child=p)


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0007_add_tableblocks_to_pages'),
    ]

    operations = [
        migrations.RunPython(create_tableblocks_for_every_table)
    ]

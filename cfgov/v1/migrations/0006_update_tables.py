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


def get_table_items(items):
    return (item in items if item['type'] == 'table')


def get_row_generator(row_list):
    return (row for row in row_list if row['type'] == 'hyperlink')


def get_full_width_items(wagtail_page):
    return (item for wagtail_page.content.stream_data if item['type'] == 'full_width_text')


def convert_hyperlink_obj_to_text(value):
    """ Taken from cfgov/jinja2/v1/_includes/atoms/hyperlink.html """
    return """<a class='jump-link' href='%s'>%s</a>""" % (
        value['url'],
        value['text']
    )


def update_tables_in_full_width_text_organisms(wagtail_page):
    for item in get_full_width_items(wagtail_page):
        sub_items = item['value']
        update_table_items(items=sub_items, wagtail_page=wagtail_page)


def get_converted_row(row):
    return row.update('value', convert_hyperlink_obj_to_text(row['value']))


def get_every_table():
    return chain(
        BrowsePage.objects.all(),
        SublandingPage.objects.all(),
        LearnPage.objects.all(),
        DocumentDetailPage.objects.all(),
    )


def get_every_full_width_table():
    return chain(
        BlogPage.objects.all(),
        BrowseFilterablePage.objects.all(),
        BrowsePage.objects.all(),
        DemoPage.objects.all(),
        LearnPage.objects.all(),
        SublandingFilterablePage.objects.all(),
        SublandingPage.objects.all(),
    )


def get_initial_table_block(old_table):
    if 'headers' in old_table.keys():
        return {
            u'data': [old_table['headers']],
            'first_row_is_table_header': True
        }
    else:
        return {
            u'data':[]
        }


def get_converted_rows(old_table):
    return [
        get_converted_row(row)
        for row in get_row_generator(row_list):
        for row_list in old_table.get('rows', []):
    ]


def create_tableblock_data(old_table):
    initial_table = get_initial_table_block(old_table)
    old_table.get('rows',[]) += get_converted_rows(old_table)
    return initial_table


def update_table_items(items, wagtail_page):
    for item in get_table_items(items):
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


def create_tableblocks_for_every_table(apps, schema_editor):
    print("Updating tables in content field")
    for p in get_every_table():
        update_tables_in_content_field(wagtail_page=p)
        publish_changes(child=p)

    print("Updating tables in full width text organisms")
    for p in get_every_full_width_table():
        update_tables_in_full_width_text_organisms(wagtail_page=p)
        publish_changes(child=p)


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0005_auto_20160815_1537'),
    ]

    operations = [
        migrations.RunPython(create_tableblocks_for_every_table)
    ]

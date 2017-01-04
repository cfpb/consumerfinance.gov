# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.db import migrations
from v1.tests.wagtail_pages.helpers import publish_changes


logger = logging.getLogger(__name__)


def update_table_items(items, wagtail_page):
    table_items = list(filter(lambda i: i['type'] == 'table', items))

    for item in table_items:
        item['type'] = 'table_block'
        item['value'] = create_tableblock_data(old_table=item['value'])
        logger.info(
            "Updating Table to a TableBlock on page %s of page type %s"
            % (wagtail_page.title, wagtail_page.__class__.__name__)
        )

    return table_items


def update_tables_in_content_field(wagtail_page):
    return update_table_items(
        items=wagtail_page.content.stream_data,
        wagtail_page=wagtail_page
    )


def update_tables_in_full_width_text_organisms(wagtail_page):
    tables = []

    for item in list(filter(
        lambda item: item['type'] == 'full_width_text',
        wagtail_page.content.stream_data
    )):
        sub_items = item['value']
        tables.extend(
            update_table_items(items=sub_items, wagtail_page=wagtail_page)
        )

    return tables


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
    logger.info('Updating tables in content field')
    cf_page_types = (
        'BrowsePage', 'SublandingPage', 'LearnPage', 'DocumentDetailPage',
    )

    for cf_page_type in cf_page_types:
        page_cls = apps.get_model('v1', cf_page_type)
        for p in page_cls.objects.all():
            if update_tables_in_content_field(wagtail_page=p):
                publish_changes(child=p)

    logger.info('Updating tables in full width text organisms')
    fwt_page_types = (
        'BlogPage', 'BrowseFilterablePage', 'BrowsePage', 'DemoPage',
        'LearnPage', 'SublandingFilterablePage', 'SublandingPage',
    )

    for fwt_page_type in fwt_page_types:
        page_cls = apps.get_model('v1', fwt_page_type)
        for p in page_cls.objects.all():
            if update_tables_in_full_width_text_organisms(wagtail_page=p):
                publish_changes(child=p)


class Migration(migrations.Migration):
    dependencies = [
        ('v1', '0012_create_tableblock'),
    ]

    operations = [
        migrations.RunPython(create_tableblocks_for_every_table)
    ]

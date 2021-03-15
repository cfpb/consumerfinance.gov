from django.shortcuts import get_object_or_404

import wagtail
from wagtail.core.models import Page
from wagtail.documents import get_document_model

from bs4 import BeautifulSoup

from v1.models.base import CFGOVPage
from v1.tests.wagtail_pages.helpers import publish_changes


def get_tableblocks(page):
    """ Get all the TableBlocks for a given page.
    TableBlocks can be stored either directly in page's content,
    or in a FullWidthText item. So we must check both.
    """
    try:
        if wagtail.VERSION < (2, 12):  # pragma: no cover
            data = page.specific.content.stream_data
        else:
            data = page.specific.content.raw_data
    except Exception:
        return []
    tableblocks = list(
        filter(lambda item: item['type'] == 'table_block', data))
    full_width_text_items = list(
        filter(lambda item: item['type'] == 'full_width_text', data))
    for item in full_width_text_items:
        sub_items = item['value']
        for sub_item in list(
                filter(lambda i: i['type'] == 'table_block', sub_items)):
            tableblocks.append(sub_item)
    return tableblocks


def convert_links(links):
    """ Adds a href to the link with the reative path if a
    document ID or page ID is stored
    """
    updated = False
    for link in links:
        linktype = link.get('linktype')
        object_id = link.get('id')
        if link.get('href'):
            continue  # Don't update it if the href is already set
        if linktype == 'document':
            doc = get_object_or_404(get_document_model(), id=object_id)
            url = doc.url
        elif linktype == 'page':
            page = Page.objects.get(id=object_id)
            url = page.relative_url(current_site=page.get_site())
        else:
            continue
        updated = True
        link['href'] = url
    return updated


def run():
    for page in CFGOVPage.objects.all():
        changes = False
        tableblocks = get_tableblocks(page)
        for tableblock in tableblocks:
            rows = tableblock['value']['data']
            for row in rows:
                for idx, item in enumerate(row):
                    if not item:
                        continue

                    soup = BeautifulSoup(item, 'html.parser')
                    links = soup.findAll('a')
                    if links and convert_links(links):
                        # Set the item to the modified HTML
                        row[idx] = str(soup)
                        changes = True
        if changes:
            publish_changes(page.specific)

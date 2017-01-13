import json
import logging
import os
from exceptions import ValueError
from urlparse import urlsplit

import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.utils.html import escape, format_html_join
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page

from .util import util

logger = logging.getLogger(__name__)


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'js/table-block.js',
    ]
    js_includes = format_html_join(
        '\n',
        '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )

    return js_includes


@hooks.register('insert_editor_css')
def editor_css():
    css_files = [
        'css/table-block.css',
        'css/bureau-structure.css'
    ]
    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}{1}"><link>',
        ((settings.STATIC_URL, filename) for filename in css_files)
    )

    return css_includes




def get_akamai_credentials():
    object_id = getattr(settings, 'AKAMAI_OBJECT_ID', None)
    user = getattr(settings, 'AKAMAI_USER', None)
    password = getattr(settings, 'AKAMAI_PASSWORD', None)

    if not all((object_id, user, password)):
        raise ValueError(
            'AKAMAI_OBJECT_ID, AKAMAI_USER, and AKAMAI_PASSWORD '
            'must be configured.'
        )

    return object_id, (user, password)


def should_flush():
    """Only initiate an Akamai flush if it is enabled in settings."""
    return settings.ENABLE_AKAMAI_CACHE_PURGE


def flush_akamai():
    if should_flush():
        object_id, auth = get_akamai_credentials()
        headers = {'content-type': 'application/json'}
        payload = {
            'action': 'invalidate',
            'type': 'cpcode',
            'domain': 'production',
            'objects': [object_id]
        }
        r = requests.post(
            settings.AKAMAI_PURGE_URL,
            headers=headers,
            data=json.dumps(payload),
            auth=auth
        )
        logger.info(
            'Initiated Akamai flush with response {text}'.format(text=r.text)
        )
        if r.status_code == 201:
            return True
    return False



class CFGovLinkHandler(object):
    """
    CFGovLinkHandler will be invoked whenever we encounter an <a> element in
    HTML content with an attribute of data-linktype="page". The resulting
    element in the database representation will be:
    <a linktype="page" id="42">hello world</a>
    """

    @staticmethod
    def get_db_attributes(tag):
        """
        Given an <a> tag that we've identified as a page link embed (because it
        has a data-linktype="page" attribute), return a dict of the attributes
        we should have on the resulting <a linktype="page"> element.
        """
        return {'id': tag['data-id']}

    @staticmethod
    def expand_db_attributes(attrs, for_editor):
        try:
            page = Page.objects.get(id=attrs['id'])

            if for_editor:
                editor_attrs = 'data-linktype="page" data-id="%d" ' % page.id
            else:
                editor_attrs = ''

            return '<a %shref="%s">' % (
                editor_attrs,
                escape(urlsplit(page.url).path)
            )
        except Page.DoesNotExist:
            return "<a>"


@hooks.register('register_rich_text_link_handler')
def register_cfgov_link_handler():
    return ('page', CFGovLinkHandler)


@hooks.register('cfgovpage_context_handlers')
def form_module_handlers(page, request, context, *args, **kwargs):
    """
    Hook function that iterates over every Streamfield's blocks on a page and
    sets the context for any form modules.
    """
    form_modules = {}
    streamfields = util.get_streamfields(page)

    for fieldname, blocks in streamfields.items():
        for index, child in enumerate(blocks):
            if hasattr(child.block, 'get_result'):
                if fieldname not in form_modules:
                    form_modules[fieldname] = {}

                if not request.method == 'POST':
                    is_submitted = child.block.is_submitted(
                        request,
                        fieldname,
                        index
                    )
                    module_context = child.block.get_result(
                        page,
                        request,
                        child.value,
                        is_submitted
                    )
                    form_modules[fieldname].update({index: module_context})

    if form_modules:
        context['form_modules'] = form_modules

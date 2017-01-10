import json
import logging
import os
from exceptions import ValueError
from urlparse import urlsplit

import requests
from django.conf import settings
from django.contrib.auth.models import Permission
from django.http import Http404
from django.utils import timezone
from django.utils.html import escape, format_html_join
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page

from .models import CFGOVPage
from .util import util

logger = logging.getLogger(__name__)


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def share_the_page(request, page):
    page = Page.objects.get(id=page.id).specific
    parent_page = page.parent()
    is_publishing = bool(request.POST.get('action-publish', False))
    is_sharing = bool(request.POST.get('action-share', False))

    check_permissions(parent_page, request.user, is_publishing, is_sharing)

    is_live = False
    goes_live_in_future = page.go_live_at and page.go_live_at > timezone.now()

    if is_publishing and not goes_live_in_future:
        is_live = True

    share(page, is_sharing, is_live)
    configure_page_revision(page, is_sharing, is_live)
    if is_live:
        flush_akamai()


@hooks.register('after_delete_page')
def log_page_deletion(request, page):
    logger.warning(
        u'User {user} with ID {user_id} deleted page {title} with ID {page_id} at URL {url}'.format(  # noqa: E501
            user=request.user,
            user_id=request.user.id,
            title=page.title,
            page_id=page.id,
            url=page.url_path,
        )
    )


def check_permissions(parent, user, is_publishing, is_sharing):
    parent_perms = parent.permissions_for_user(user)
    if parent.slug != 'root':
        is_publishing = is_publishing and parent_perms.can_publish()
        is_sharing = is_sharing and parent_perms.can_publish()


def share(page, is_sharing, is_live):
    if is_sharing or is_live:
        page.shared = True
        page.has_unshared_changes = False
    else:
        page.has_unshared_changes = True
    page.save()


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


# `CFGOVPage.route()` will select the latest revision of the page where `live`
# is set to True and return that revision as a page object to serve the request
# so here we configure the latest revision to fall in line with that logic.
#
# This is also used as a signal callback when publishing in code or via
# management command like publish_scheduled_pages.
def configure_page_revision(page, is_sharing, is_live):
    latest = page.get_latest_revision()
    content_json = json.loads(latest.content_json)
    content_json['live'] = is_live
    content_json['shared'] = is_sharing or is_live
    content_json['has_unshared_changes'] = not is_sharing and not is_live
    latest.content_json = json.dumps(content_json)
    latest.save()


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


@hooks.register('before_serve_page')
def check_request_site(page, request, serve_args, serve_kwargs):
    if request.site.hostname == os.environ.get('DJANGO_STAGING_HOSTNAME'):
        if isinstance(page, CFGOVPage):
            if not page.shared:
                raise Http404


@hooks.register('register_permissions')
def register_share_permissions():
    return Permission.objects.filter(codename='share_page')


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

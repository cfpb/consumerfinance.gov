import os
import json
from urlparse import urlsplit
from django.utils import timezone

from django.conf import settings
from django.http import Http404
from django.contrib.auth.models import Permission
from django.utils.html import escape

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore import hooks

from .models import CFGOVPage
from .models.handlers import Handler
from .models.handlers.filterable_list_handlers import FilterableListHandler, \
    EventArchiveHandler, NewsroomHandler, ActivityLogHandler
from .models.handlers.js_handler import JSHandler


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def share_the_page(request, page):
    page = Page.objects.get(id=page.id).specific
    parent_page = page.parent()
    is_publishing = bool(request.POST.get('action-publish', False))
    is_sharing = bool(request.POST.get('action-share', False))

    check_permissions(parent_page, request.user, is_publishing, is_sharing)

    is_live = False
    if is_publishing and not (page.go_live_at and page.go_live_at > timezone.now()):
        is_live = True

    share(page, is_sharing, is_live)
    configure_page_revision(page, is_sharing, is_live)
    flush_akamai(page, is_live)


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


def flush_akamai(page, is_live):
    if is_live and settings.ENABLE_AKAMAI_CACHE_PURGE:
        from publish_eccu.publish import publish as akamai_cache_reset

        url_paths = [page.url_path.replace('cfgov/', '')]
        if url_paths[0] == '/':
            is_home_page = True
        else:
            is_home_page = False

        akamai_cache_reset(url_paths, invalidate_root=is_home_page, user_email=page.owner.email)


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
    CFGovLinkHandler will be invoked whenever we encounter an <a> element in HTML content
    with an attribute of data-linktype="page". The resulting element in the database
    representation will be:
    <a linktype="page" id="42">hello world</a>
    """

    @staticmethod
    def get_db_attributes(tag):
        """
        Given an <a> tag that we've identified as a page link embed (because it has a
        data-linktype="page" attribute), return a dict of the attributes we should
        have on the resulting <a linktype="page"> element.
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

            return '<a %shref="%s">' % (editor_attrs, escape(urlsplit(page.url).path))
        except Page.DoesNotExist:
            return "<a>"


@hooks.register('register_rich_text_link_handler')
def register_cfgov_link_handler():
    return ('page', CFGovLinkHandler)


@hooks.register('cfgov_context_handlers')
def register_js_handler(*args):
    handler = JSHandler(*args)
    handler.process()


@hooks.register('cfgov_context_handlers')
def register_filterablelist_handlers(*args):
    base_handler = Handler(*args)
    def get_filter_blocks():
        block_tuples = []
        blocks_dict = base_handler.get_streamfield_blocks()
        for blocks_list in blocks_dict.values():
            for form_id, block in enumerate(blocks_list):
                if block.block_type == 'filter_controls':
                    block_tuples.append((form_id, block))
        return block_tuples

    block_tuples = get_filter_blocks()
    if block_tuples:
        i, block = block_tuples[0]
        page_type = block.value['page_type']
        if page_type == 'newsroom':
            handler = NewsroomHandler(*args)
        elif page_type == 'activity-log':
            handler = ActivityLogHandler(*args)
        elif page_type == 'event-archive':
            handler = EventArchiveHandler(*args)
        else:
            handler = FilterableListHandler(*args)
        handler.process(block_tuples)

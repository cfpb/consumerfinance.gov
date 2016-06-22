import os
import json
from urlparse import urlsplit

from django.conf import settings
from django.http import Http404
from django.contrib.auth.models import Permission
from django.utils.html import escape

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore import hooks

from v1.models import CFGOVPage


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def share_the_page(request, page):
    page = Page.objects.get(id=page.id).specific
    parent_page = page.parent()
    is_publishing = bool(request.POST.get('action-publish', False))
    is_sharing = bool(request.POST.get('action-share', False))

    check_permissions(parent_page, request.user, is_publishing, is_sharing)
    share(page, is_sharing, is_publishing)
    configure_page_revision(page, is_sharing, is_publishing)


def check_permissions(parent, user, is_publishing, is_sharing):
    parent_perms = parent.permissions_for_user(user)
    if parent.slug != 'root':
        is_publishing = is_publishing and parent_perms.can_publish()
        is_sharing = is_sharing and parent_perms.can_publish()


def share(page, is_sharing, is_publishing):
    if is_sharing or is_publishing:
        page.shared = True
        page.has_unshared_changes = False
    else:
        page.has_unshared_changes = True
    page.save()


# Sets the latest revision with a state depending on if the request is to
# publish, share, or save the page.
def configure_page_revision(page, is_sharing, is_publishing):
    latest = page.get_latest_revision()
    content_json = json.loads(latest.content_json)
    content_json['live'] = is_publishing
    content_json['shared'] = is_sharing or is_publishing
    content_json['has_unshared_changes'] = page.has_unshared_changes
    latest.content_json = json.dumps(content_json)
    latest.save()
    if is_publishing:
        latest.publish()
        if settings.ENABLE_AKAMAI_CACHE_PURGE:
            from publish_eccu.publish import publish as akamai_cache_reset

            url_paths = [page.url_path.replace('cfgov/', '')]
            if url_paths[0] == '/':
                is_home_page = True
            else:
                is_home_page = False

            akamai_cache_reset(url_paths, invalidate_root=is_home_page, user_email=latest.user.email)


@hooks.register('before_serve_page')
def check_request_site(page, request, serve_args, serve_kwargs):
    if request.site.hostname == os.environ.get('STAGING_HOSTNAME'):
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

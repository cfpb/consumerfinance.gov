import os
import json
from urlparse import urlsplit

from django.http import Http404
from django.contrib.auth.models import Permission
from django.utils.html import escape

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore import hooks

from v1.models import CFGOVPage


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def share_the_page(request, page):
    page = page.specific
    parent_page = page.parent()
    parent_page_perms = parent_page.permissions_for_user(request.user)

    if parent_page.slug != 'root':
        is_publishing = bool(request.POST.get('action-publish')) and parent_page_perms.can_publish()
        is_sharing = bool(request.POST.get('action-share')) and parent_page_perms.can_publish()
    else:  # Giving Root page permissions to publish/share
        is_publishing = bool(request.POST.get('action-publish'))
        is_sharing = bool(request.POST.get('action-share'))

    # If the page is being shared or published, set `shared` to True or else False
    # and save the page.
    if is_sharing or is_publishing:
        page.shared = True
    else:
        page.shared = False
    page.save()

    # If the page isn't being published but the page is live and the editor
    # wants to share updated content that doesn't show on the production site,
    # we must set the page.live to True, delete the latest revision, and save
    # a new revision with `live` = False. This doesn't affect the page's published
    # status, as the saved page object in the database still has `live` equal to
    # True and we're never commiting the change. As seen in CFGOVPage's route
    # method, `route()` will select the latest revision of the page where `live`
    # is set to True and return that revision as a page object to serve the request with.
    if not is_publishing:
        page.live = False
    latest = page.get_latest_revision()
    content_json = json.loads(latest.content_json)
    content_json['live'], content_json['shared'] = page.live, page.shared
    latest.content_json = json.dumps(content_json)
    latest.save()
    if is_publishing:
        latest.publish()


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

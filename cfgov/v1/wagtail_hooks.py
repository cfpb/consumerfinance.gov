import json
import logging

from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.html import escape, format_html_join
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin import widgets as wagtailadmin_widgets
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page
from urlparse import urlsplit

from v1.templatetags.share import v1page_permissions
from v1.util import util

from akamai.edgegrid import EdgeGridAuth


logger = logging.getLogger(__name__)


@hooks.register('before_delete_page')
def raise_delete_error(request, page):
    raise PermissionDenied('Deletion via POST is disabled')


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


@hooks.register('after_delete_page')
def log_page_deletion(request, page):
    logger.warning(
        (
            u'User {user} with ID {user_id} deleted page {title} '
            u'with ID {page_id} at URL {url}'
        ).format(
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
        'css/richtext.css',
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
    client_token = getattr(settings, 'AKAMAI_CLIENT_TOKEN', None)
    client_secret = getattr(settings, 'AKAMAI_CLIENT_SECRET', None)
    access_token = getattr(settings, 'AKAMAI_ACCESS_TOKEN', None)
    fast_purge_url = getattr(settings, 'AKAMAI_FAST_PURGE_URL', None)
    if not all((client_token, client_secret, access_token, fast_purge_url)):
        raise ValueError(
            'AKAMAI_CLIENT_TOKEN, AKAMAI_CLIENT_SECRET, AKAMAI_ACCESS_TOKEN,'
            ' AKAMAI_FAST_PURGE_URL must be configured.'
        )
    auth = EdgeGridAuth(
        client_token=client_token,
        client_secret=client_secret,
        access_token=access_token
    )
    return auth, fast_purge_url


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


@hooks.register('register_admin_menu_item')
def register_django_admin_menu_item():
    return MenuItem(
        'Django Admin',
        reverse('admin:index'),
        classnames='icon icon-redirect',
        order=99999
    )


@hooks.register('register_page_listing_more_buttons')
def page_listing_more_buttons(page, page_perms, is_parent=False):
    page = page.specific

    context = {'request': type('obj', (object,), {'user': page_perms.user})}
    v1_page_perms = v1page_permissions(context, page)

    shared = getattr(page, 'shared', False)
    if shared and not page.live and v1_page_perms.can_unshare():
        yield wagtailadmin_widgets.Button(
            _('Unshare'), reverse('unshare', args=[page.id]),
            attrs={"title": _('Unshare this page')}, priority=41
        )

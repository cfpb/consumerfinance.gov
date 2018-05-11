import logging
from six.moves.urllib.parse import urlsplit

from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.html import escape, format_html_join

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.rich_text import PageLinkHandler

from v1.util import util


logger = logging.getLogger(__name__)


@hooks.register('before_delete_page')
def raise_delete_error(request, page):
    raise PermissionDenied('Deletion via POST is disabled')


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
        'css/general-enhancements.css',
        'css/table-block.css',
        'css/bureau-structure.css',
        'css/heading-block.css',
        'css/info-unit-group.css',
    ]
    css_includes = format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}{1}"><link>',
        ((settings.STATIC_URL, filename) for filename in css_files)
    )

    return css_includes


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


class RelativePageLinkHandler(PageLinkHandler):
    """
    Rich text link handler that forces all page links to be relative.

    This special page link handler makes it so that any internal Wagtail page
    links inserted into rich text fields are rendered as relative links.

    Standard Wagtail behavior stores rich text link content in the database in
    a psuedo-HTML format like this, including only a page's ID:

        <a linktype="page" id="123">foo</a>

    When this content is rendered for preview or viewing, it's replaced with
    valid HTML including the page's URL. This custom handler ensures that page
    URLs are always rendered as relative, like this:

        <a href="/path/to/page">foo</a>

    Pages rendered with this handler should never be rendered like this:

        <a href="https://my.domain/path/to/page">foo</a>

    In standard Wagtail behavior, pages will be rendered with an absolute URL
    if an installation has multiple Wagtail Sites. In our current custom usage
    we have multiple Wagtail Sites (one for production, one for staging) that
    share the same root page. So forcing the use of relative URLs would work
    fine and allow for easier navigation within a single domain.

    This will explicitly break things if users ever wanted to host some
    additional site that doesn't share the same root page.

    This code is modified from `wagtail.wagtailcore.rich_text.PageLinkHandler`.
    """
    @staticmethod
    def expand_db_attributes(attrs, for_editor):
        try:
            page = Page.objects.get(id=attrs['id'])

            if for_editor:
                editor_attrs = 'data-linktype="page" data-id="%d" ' % page.id
                parent_page = page.get_parent()
                if parent_page:
                    editor_attrs += 'data-parent-id="%d" ' % parent_page.id
            else:
                editor_attrs = ''

            page_url = page.specific.url

            if page_url:
                page_url = urlsplit(page_url).path

            return '<a %shref="%s">' % (editor_attrs, escape(page_url))
        except Page.DoesNotExist:
            return "<a>"


@hooks.register('register_rich_text_link_handler')
def register_cfgov_link_handler():
    return ('page', RelativePageLinkHandler)


@hooks.register('register_admin_menu_item')
def register_frank_menu_item():
    return MenuItem('CDN Tools',
                    reverse('manage-cdn'),
                    classnames='icon icon-cogs',
                    order=10000)


@hooks.register('register_admin_urls')
def register_flag_admin_urls():
    handler = 'v1.admin_views.manage_cdn'
    return [url(r'^cdn/$', handler, name='manage-cdn'), ]


@hooks.register('before_serve_page')
def serve_latest_draft_page(page, request, args, kwargs):
    if page.pk in settings.SERVE_LATEST_DRAFT_PAGES:
        latest_draft = page.get_latest_revision_as_page()
        response = latest_draft.serve(request, *args, **kwargs)
        response['Serving-Wagtail-Draft'] = '1'
        return response

import os, itertools

from django.http import Http404
from django.contrib.auth.models import Permission
from django.core.management import call_command
from v1.models import CFGOVPage

from wagtail.wagtailcore import hooks

from v1.util import js_routes


@hooks.register('after_create_page')
@hooks.register('after_edit_page')
def share_the_page(request, page):
    page = page.specific
    parent_page = page.get_ancestors(inclusive=False).reverse()[0].specific
    parent_page_perms = parent_page.permissions_for_user(request.user)

    is_publishing = bool(request.POST.get('action-publish')) and parent_page_perms.can_publish()
    is_sharing = bool(request.POST.get('action-share')) and parent_page_perms.can_publish()

    if is_sharing or is_publishing:
        page.shared = True
    else:
        page.shared = False

    page.save()
    revision = page.save_revision()
    if is_publishing:
        revision.publish()

    build_js_routes(request, page)


@hooks.register('before_serve_page')
def check_request_site(page, request, serve_args, serve_kwargs):
    if request.site.hostname == os.environ.get('STAGING_HOSTNAME'):
        if isinstance(page, CFGOVPage):
            if not page.shared:
                raise Http404


def build_js_routes(request, page):
    elements = []

    if hasattr(page, 'demopage'):
        chain = itertools.chain(page.organisms.stream_data, page.molecules.stream_data)
    if hasattr(page, 'landingpage'):
        chain = itertools.chain(page.hero.stream_data,
                                page.introduction.stream_data,
                                page.image_text_25_75_content.stream_data,
                                page.image_text_50_50_content.stream_data,
                                page.half_width_link_blob_content.stream_data,
                                page.wells.stream_data
                                )

    children = list(chain)
    for child in children:
        elements.append(child[0])

    data = {
        'slug': str(page.url),
        'elements': elements
    }

    if js_routes.create_route(data):
        call_command('build-routes')


@hooks.register('after_delete_page')
def delete_key_pages_json(request, page):
    if js_routes.create_route(data):
        js_routes.delete_route(page.url)

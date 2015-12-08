import os, json, itertools

from django.conf import settings
from django.http import Http404
from django.contrib.auth.models import Permission

from wagtail.wagtailcore import hooks

from v1.models import CFGOVPage


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

    update_pages_json(request, page)


@hooks.register('before_serve_page')
def check_request_site(page, request, serve_args, serve_kwargs):
    if request.site.hostname == os.environ.get('STAGING_HOSTNAME'):
        if isinstance(page, CFGOVPage):
            if not page.shared:
                raise Http404


@hooks.register('register_permissions')
def register_share_permissions():
    return Permission.objects.filter(codename='share_page')


def update_pages_json(request, page):
    page = page.specific

    data = json.load(open(settings.PROJECT_ROOT.child('v1') + '/pages.json'))

    # Base page doesn't have a generic ALL children object so you must create cases for each
    # repetitive

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

    data['page_' + str(page.id)] = {
        'slug': str(page.slug),
        'elements': elements
    }

    with open(settings.PROJECT_ROOT.child('v1') + '/pages.json', 'w') as outfile:
        json.dump(data, outfile)

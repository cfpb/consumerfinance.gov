import collections, json, os, re
from itertools import chain
from time import time
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import resolve
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.blocks.struct_block import StructValue
from ref import related_posts_categories

def get_unique_id(prefix='', suffix=''):
    index = hex(int(time() * 10000000))[2:]
    return prefix + str(index) + suffix

# These messages are manually mirrored on the
# Javascript side in error-messages-config.js

ERROR_MESSAGES = {
    'CHECKBOX_ERRORS': {
        'required': 'Please select at least one of the "%s" options.'
    },
    'DATE_ERRORS': {
        'invalid': 'You have entered an invalid date: %s.',
        'one_required': 'Please enter at least one date.'
    }
}

def get_form_id(page):
    for i, block in enumerate(page.content):
        if block.block_type == 'filter_controls':
            return i
    return 0


def instanceOfBrowseOrFilterablePages(page):
    from ..models import BrowsePage, BrowseFilterablePage
    return isinstance(page, (BrowsePage, BrowseFilterablePage))


# For use by Browse type pages to get the secondary navigation items
# TODO: Move into BrowsePage class once BrowseFilterablePage has been merged
# into BrowsePage
def get_secondary_nav_items(request, current_page):
    from ..templatetags.share import get_page_state_url
    on_staging = os.environ.get('DJANGO_STAGING_HOSTNAME') == request.site.hostname
    nav_items = []
    parent = current_page.get_parent().specific
    if instanceOfBrowseOrFilterablePages(parent):
        page = get_appropriate_page_version(request, parent)
    else:
        page = get_appropriate_page_version(request, current_page)

    if not page:
        return [], False

    # TODO: Remove this ASAP once Press Resources gets its own Wagtail page
    if page.slug == 'newsroom':
        return [
            {
                'title': page.title,
                'slug': page.slug,
                'url': get_page_state_url({}, page),
                'children': [
                    {
                        'title': 'Press Resources',
                        'slug': 'press-resources',
                        'url': '/newsroom/press-resources/',
                    }
                ],
            }
        ], True
    # END TODO

    pages = [page] if page.secondary_nav_exclude_sibling_pages else page.get_appropriate_siblings(request.site.hostname)

    for sibling in pages:
        # Only if it's a Browse(Filterable) type page
        if instanceOfBrowseOrFilterablePages(sibling.specific):
            if page.id == sibling.id:
                sibling = get_appropriate_page_version(request, page)
            else:
                sibling = get_appropriate_page_version(request, sibling)
            item = {
                'title': sibling.title,
                'slug': sibling.slug,
                'url': get_page_state_url({}, sibling),
                'children': [],
            }
            children = sibling.get_children().specific()
            for child in [c for c in children if (on_staging and c.shared) or c.live]:
                if instanceOfBrowseOrFilterablePages(child):
                    item['children'].append({
                        'title': child.title,
                        'slug': child.slug,
                        'url': get_page_state_url({}, child),
                    })
            nav_items.append(item)
    # Return a boolean about whether or not the current page has Browse children
    for item in nav_items:
        if get_page_state_url({}, page) == item['url'] and item['children']:
            return nav_items, True
    return nav_items, False


def get_appropriate_page_version(request, page):
    # If we're on the production site, make sure the version of the page
    # displayed is the latest version that has `live` set to True for
    # the live site or `shared` set to True for the staging site.
    staging_hostname = os.environ.get('DJANGO_STAGING_HOSTNAME')
    revisions = page.revisions.all().order_by('-created_at')
    for revision in revisions:
        page_version = json.loads(revision.content_json)
        if request.site.hostname != staging_hostname:
            if page_version['live']:
                return revision.as_page_object()
        else:
            if page_version['shared']:
                return revision.as_page_object()

def valid_destination_for_request(request, url):

    view, args, kwargs = resolve(url)
    kwargs['request'] = request
    try:
        response = view(*args, **kwargs)
    except (Http404, TypeError):
        return False

    if isinstance(response, HttpResponseRedirect):
        # this indicates a permissions problem
        # (there may be a better way)
        if REDIRECT_FIELD_NAME + '=' in response.url:
            return False

    return True


def all_valid_destinations_for_request(request):
    possible_destinations = (('Wagtail','/admin/'), ('Django admin', '/django-admin/'))
    valid_destinations = [pair for pair in possible_destinations if
                            valid_destination_for_request(request, pair[1])]

    return valid_destinations


def has_active_filters(request, index):
    for key, param in request.GET.items():
        if key != 'form-id':
            if str(index) in key and param:
                return True
    return False

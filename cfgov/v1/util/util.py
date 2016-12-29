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
        'invalid': 'You have entered an invalid date.',
    }
}

def instanceOfBrowseOrFilterablePages(page):
    from ..models import BrowsePage, BrowseFilterablePage
    return isinstance(page, (BrowsePage, BrowseFilterablePage))


# For use by Browse type pages to get the secondary navigation items
# TODO: Move into BrowsePage class once BrowseFilterablePage has been merged
# into BrowsePage
def get_secondary_nav_items(request, current_page):
    from v1.templatetags.share import get_page_state_url
    on_staging = os.environ.get('DJANGO_STAGING_HOSTNAME') == request.site.hostname
    nav_items = []
    parent = current_page.get_parent().specific
    if instanceOfBrowseOrFilterablePages(parent):
        page = parent.get_appropriate_page_version(request)
    else:
        page = current_page.get_appropriate_page_version(request)

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

    # TODO: Remove this ASAP once the-bureau gets migrated to Wagtail
    if page.slug == 'leadership-calendar':
        BASE_URL = '/about-us/the-bureau'
        return [{
                'title': 'The Bureau',
                'slug': 'the-bureau',
                'url': '/the-bureau/',
                'children': [{
                    'title': 'The Director',
                    'url': BASE_URL + '/about-director/',
                    'slug': 'about-director',
                },{
                    'title': 'The Deputy Director',
                    'url': BASE_URL + '/about-deputy-director/',
                    'slug': 'about-deputy-director',
                },{
                    'title': 'Bureau Structure',
                    'url': BASE_URL + '/bureau-structure/',
                    'slug': 'bureau-structure',
                },{
                    'title': page.title,
                    'url': get_page_state_url({}, page).replace('/about-us', BASE_URL),
                    'slug': page.slug,
                }]
        }], True
    # END TODO

    pages = [page] if page.secondary_nav_exclude_sibling_pages else page.get_appropriate_siblings(request.site.hostname)

    for sibling in pages:
        # Only if it's a Browse(Filterable) type page
        if instanceOfBrowseOrFilterablePages(sibling.specific):
            if page.id == sibling.id:
                sibling = page.get_appropriate_page_version(request)
            else:
                sibling = sibling.get_appropriate_page_version(request)
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


def get_streamfields(page):
    """
    Retrieves the stream values on a page from its Streamfield
    """
    blocks_dict = {}
    for key, value in vars(page).items():
        if isinstance(value, StreamValue):
            blocks_dict.update({key: value})
    return blocks_dict

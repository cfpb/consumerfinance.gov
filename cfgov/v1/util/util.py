import collections
import re
import os
from itertools import chain
from time import time
from django.conf import settings
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.blocks.struct_block import StructValue
from ref import related_posts_categories

def id_validator(id_string, search=re.compile(r'[^a-zA-Z0-9-_]').search):
    if id_string:
        return not bool(search(id_string))
    else:
        return False


# example_case ==> ExampleCase
def to_camel_case(snake_str):
    snake_str = snake_str.capitalize()
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


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
        'one_required': 'Please enter at least one date.'
    }
}


def get_related_posts_categories(category):
    if category:
        cats = dict(related_posts_categories)
        for key, value in cats.iteritems():
            sub_cats = dict(value)

            if category in sub_cats:
                if key == 'Blog':
                    return 'posts'
                elif key == 'Newsroom':
                    return 'newsroom'


# Orders by most to least common in the given list.
def most_common(lst):
    # Returns the lst if empty or there's just one element in it.
    if not lst or len(lst) == 1:
        return lst
    else:
        # Gets the most common element in the list.
        most = max(set(lst), key=lst.count)
        # Creates a new list without that element.
        new_list = [e for e in lst if most not in e]
        # Recursively returns a list with the most common elements ordered
        # most to least. Ties go to the lowest index in the given list.
        return [most] + most_common(new_list)


def get_form_id(page, get_request):
    from filterable_context import get_form_specific_filter_data

    form_ids = []

    form_ids = get_form_specific_filter_data(page, page.get_form_class(),
                                                      get_request).keys()
    if form_ids:
        return form_ids[0]
    else:
        return 0


def instanceOfBrowseOrFilterablePages(page):
    from ..models import BrowsePage, BrowseFilterablePage
    return isinstance(page, BrowsePage, BrowseFilterablePage)


# For use by Browse type pages to get the secondary navigation items
def get_secondary_nav_items(current, hostname, exclude_siblings=False):
    from ..templatetags.share import get_page_state_url
    on_staging = os.environ.get('STAGING_HOSTNAME') == hostname
    nav_items = []
    parent = current.get_parent().specific
    page = parent if instanceOfBrowseOrFilterablePages(parent) else current

    pages = [page] if page.secondary_nav_exclude_sibling_pages else page.get_appropriate_siblings(hostname)

    for sibling in pages:
        # Only if it's a Browse type page
        if 'Browse' in sibling.specific_class.__name__:
            sibling = page if page.id == sibling.id else sibling
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

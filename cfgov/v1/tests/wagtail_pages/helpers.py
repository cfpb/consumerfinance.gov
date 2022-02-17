import json
from datetime import date

from django.core.exceptions import ValidationError
from django.http import Http404

from wagtail.core.models import Site

from v1.models.base import CFGOVPageCategory
from v1.models.blog_page import BlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.home_page import HomePage
from v1.models.landing_page import LandingPage
from v1.models.learn_page import LearnPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.sublanding_page import SublandingPage


def save_page(page):
    page.save()
    return page.save_revision()


def save_new_page(child, root=None):
    if not root:
        root = HomePage.objects.get(title='CFGov')
    root.add_child(instance=child)
    return save_page(page=child)


def publish_page(child):
    revision = save_new_page(child=child)
    revision.publish()


def publish_changes(child):
    revision = save_page(page=child)
    revision.publish()


def get_parent_route(site, parent_path=None):
    # return list of route paths
    root = site.root_page
    # since parent was not provided, make root
    parent = root
    # if a parent path is provided, use that as parent
    if parent_path:
        path_components = [
            component for component in parent_path.split('/') if component
        ]

        try:
            route = root.route(None, path_components)
        except Http404:
            return

        parent = route.page

    return parent


def create_landing_page(page_title, page_slug, parent_path=None,
                        has_email_signup=False, email_gd_code="USCFPB_000"):
    # get the current site
    site = Site.objects.get(is_default_site=True)
    # create a new page and set it as the child of an existing page
    parent = get_parent_route(site, parent_path)

    # skip if parent is None
    if not parent:
        print("skipping page creation")
        return

    # create page, add it as a child of parent, save, and publish
    new_page = LandingPage(title=page_title, slug=page_slug)
    # update sidefoot streamfield if required
    if has_email_signup:
        new_page.sidefoot = json.dumps([
            {'type': 'email_signup', 'value': {'gd_code': email_gd_code}}
        ])

    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")
        return

    # return path
    return new_page.get_url(None, site)


def create_sublanding_filterable_page(page_title, page_slug,
                                      parent_path=None,
                                      has_filter=True,
                                      filter_is_expanded=False):
    # create a new page and set it as the child of an existing page
    # get the current site
    site = Site.objects.get(is_default_site=True)
    # create a new page and set it as the child of an existing page
    parent = get_parent_route(site, parent_path)

    # skip if parent is None
    if not parent:
        print("skipping page creation")
        return

    # create page, add it as a child of parent, save, and publish
    new_page = SublandingFilterablePage(title=page_title, slug=page_slug)

    # if page has a filter, add it
    if has_filter:
        new_page.content = json.dumps([{
            'type': 'filter_controls',
            'value': {
                'is_expanded': filter_is_expanded,
                'categories': {'page_type': 'blog'},
                'topic_filtering': 'sort_alphabetically',
                'language': True,
            }
        }])

    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")
        return

    # return path
    return new_page.get_url(None, site)


def create_blog_page(page_title, page_slug, parent_path=None,
                     page_tags={}, page_categories={},
                     page_language='en',
                     date_published_override=date.today()):
    # create a new page and set it as the child of an existing page
    # get the current site
    site = Site.objects.get(is_default_site=True)
    # create a new page and set it as the child of an existing page
    parent = get_parent_route(site, parent_path)

    # skip if parent is None
    if not parent:
        print("skipping page creation")
        return

    # check for optional variables set to None
    if not page_language:
        page_language = 'en'
    if not page_tags:
        page_tags = {}
    if not page_categories:
        page_categories = {}
    if not date_published_override:
        date_published_override = date.today()

    # create page, add it as a child of parent, save, and publish
    new_page = BlogPage(title=page_title, slug=page_slug,
                        language=page_language,
                        date_published=date_published_override)

    # add tags and categories
    for item in page_tags:
        new_page.tags.add(item)
    for item in page_categories:
        new_page.categories.add(CFGOVPageCategory(name=item))

    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")
        return

    # return path
    return new_page.get_url(None, site)


def create_browse_filterable_page(page_title, page_slug, parent_path=None,
                                  has_filter=True, filter_is_expanded=False):
    # create a new page and set it as the child of an existing page
    # get the current site
    site = Site.objects.get(is_default_site=True)
    # create a new page and set it as the child of an existing page
    parent = get_parent_route(site, parent_path)

    # skip if parent is None
    if not parent:
        print("skipping page creation")
        return

    # create page, add it as a child of parent, save, and publish
    new_page = BrowseFilterablePage(title=page_title, slug=page_slug)

    # if page has a filter, add it
    if has_filter:
        new_page.content = json.dumps([{
            'type': 'filter_controls',
            'value': {
                'is_expanded': filter_is_expanded,
                'categories': {'page_type': 'research-reports'},
                'topic_filtering': 'sort_alphabetically',
                'language': True,
            }
        }])

    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")
        return

    # return path
    return new_page.get_url(None, site)


def create_learn_page(page_title, page_slug, parent_path=None,
                      page_tags={}, page_categories={},
                      date_published_override=date.today()):
    # create a new page and set it as the child of an existing page
    # get the current site
    site = Site.objects.get(is_default_site=True)
    # create a new page and set it as the child of an existing page
    parent = get_parent_route(site, parent_path)

    # skip if parent is None
    if not parent:
        print("skipping page creation")
        return

    # set date published override if set to None
    if not page_tags:
        page_tags = {}
    if not page_categories:
        page_categories = {}
    if not date_published_override:
        date_published_override = date.today()

    # create page, add it as a child of parent, save, and publish
    new_page = LearnPage(title=page_title, slug=page_slug,
                         date_published=date_published_override)

    # add tags and categories
    for item in page_tags:
        new_page.tags.add(item)
    for item in page_categories:
        new_page.categories.add(CFGOVPageCategory(name=item))

    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")
        return

    # return path
    return new_page.get_url(None, site)


def create_sublanding_page(page_title, page_slug, parent_path=None,
                           has_feedback=False):
    # create a new page and set it as the child of an existing page
    # get the current site
    site = Site.objects.get(is_default_site=True)
    # create a new page and set it as the child of an existing page
    parent = get_parent_route(site, parent_path)

    # skip if parent is None
    if not parent:
        print("skipping page creation")
        return

    # create page, add it as a child of parent, save, and publish
    new_page = SublandingPage(title=page_title, slug=page_slug)

    # if page has feedback, add it
    if has_feedback:
        new_page.content = json.dumps([{
            'type': 'feedback',
            'value': {'intro_text': 'foo'}
        }])

    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")
        return

    # return path
    return new_page.get_url(None, site)


def create_browse_page(page_title, page_slug, parent_path=None,
                       has_chart_block=False, chart_block_title='Chart',
                       chart_block_chart_type='line',
                       chart_block_color_scheme='green',
                       chart_block_data_source='',
                       chart_block_description='A chart'):
    # create a new page and set it as the child of an existing page
    # get the current site
    site = Site.objects.get(is_default_site=True)
    # create a new page and set it as the child of an existing page
    parent = get_parent_route(site, parent_path)

    # skip if parent is None
    if not parent:
        print("skipping page creation")
        return

    # create page, add it as a child of parent, save, and publish
    new_page = BrowsePage(title=page_title, slug=page_slug)

    # if page has a filter, add it
    if has_chart_block:
        date = '2022-01-01'
        new_page.content = json.dumps([{
            'type': 'chart_block', 'value': {
                'title': chart_block_title,
                'chart_type': chart_block_chart_type,
                'color_scheme': chart_block_color_scheme,
                'data_source': chart_block_data_source,
                'description': chart_block_description,
                'date_published': date,
                'last_updated_projected_data': date
            }
        }])

    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")
        return

    # return path
    return new_page.get_url(None, site)

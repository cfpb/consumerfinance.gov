from datetime import date

from django.apps import apps
from django.http import Http404
from django.core.exceptions import ValidationError

from wagtail.core.models import Site

from v1.models.home_page import HomePage
from v1.models.landing_page import LandingPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage
from v1.models.blog_page import BlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.browse_page import BrowsePage
from v1.models.learn_page import LearnPage
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

def create_landing_page(page_title, page_slug, parent_path=None):
    # create a new page and set it as the child of an existing page
    # return list of route paths
    # get the root of the current site
    site_model = apps.get_model('wagtailcore', 'Site')
    site = site_model.objects.get(is_default_site=True)
    root = site.root_page
    # since parent was not provided, make root
    parent = root
    # if a parent path is provided, use that as parent
    if parent_path:
        path_components = [component for component in parent_path.split('/') if component]

        try:
            route = root.route(None, path_components)
        except Http404:
            print("skipping page creation")

        parent = route.page

    # create page, add it as a child of parent, save, and publish
    new_page = LandingPage(title=page_title, slug=page_slug)
    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")

    # return path
    return new_page.get_url(None, site)

def create_sublanding_filterable_page(page_title, page_slug, parent_path=None):
    # create a new page and set it as the child of an existing page
    # return list of route paths
    # get the root of the current site
    site_model = apps.get_model('wagtailcore', 'Site')
    site = site_model.objects.get(is_default_site=True)
    root = site.root_page
    # since parent was not provided, make root
    parent = root
    # if a parent path is provided, use that as parent
    if parent_path:
        path_components = [component for component in parent_path.split('/') if component]

        try:
            route = root.route(None, path_components)
        except Http404:
            print("skipping page creation")

        parent = route.page

    # create page, add it as a child of parent, save, and publish
    new_page = SublandingFilterablePage(title=page_title, slug=page_slug)
    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")

    # return path
    return new_page.get_url(None, site)

def create_blog_page(page_title, page_slug, parent_path=None, page_language='en', date_published_override=date.today()):
    # create a new page and set it as the child of an existing page
    # return list of route paths
    # get the root of the current site
    site_model = apps.get_model('wagtailcore', 'Site')
    site = site_model.objects.get(is_default_site=True)
    root = site.root_page
    # since parent was not provided, make root
    parent = root

    # check for optional variables
    if not page_language:
        page_language='en'
    if not date_published_override:
        date_published_override=date.today()

    # if a parent path is provided, use that as parent
    if parent_path:
        path_components = [component for component in parent_path.split('/') if component]

        try:
            route = root.route(None, path_components)
        except Http404:
            print("skipping page creation")

        parent = route.page

    # create page, add it as a child of parent, save, and publish
    new_page = BlogPage(title=page_title, slug=page_slug, language=page_language, date_published=date_published_override)
    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")

    # return path
    return new_page.get_url(None, site)

def create_browse_filterable_page(page_title, page_slug, parent_path=None):
    # create a new page and set it as the child of an existing page
    # return list of route paths
    # get the root of the current site
    site_model = apps.get_model('wagtailcore', 'Site')
    site = site_model.objects.get(is_default_site=True)
    root = site.root_page
    # since parent was not provided, make root
    parent = root
    # if a parent path is provided, use that as parent
    if parent_path:
        path_components = [component for component in parent_path.split('/') if component]

        try:
            route = root.route(None, path_components)
        except Http404:
            print("skipping page creation")

        parent = route.page

    # create page, add it as a child of parent, save, and publish
    new_page = BrowseFilterablePage(title=page_title, slug=page_slug)
    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")

    # return path
    return new_page.get_url(None, site)

def create_learn_page(page_title, page_slug, parent_path=None, date_published_override=date.today()):
    # create a new page and set it as the child of an existing page
    # return list of route paths
    # get the root of the current site
    site_model = apps.get_model('wagtailcore', 'Site')
    site = site_model.objects.get(is_default_site=True)
    root = site.root_page

    # set date published override if set to None
    if not date_published_override:
        date_published_override=date.today()

    # since parent was not provided, make root
    parent = root
    # if a parent path is provided, use that as parent
    if parent_path:
        path_components = [component for component in parent_path.split('/') if component]

        try:
            route = root.route(None, path_components)
        except Http404:
            print("skipping page creation")

        parent = route.page

    # create page, add it as a child of parent, save, and publish
    new_page = LearnPage(title=page_title, slug=page_slug, date_published=date_published_override)
    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")

    # return path
    return new_page.get_url(None, site)

def create_sublanding_page(page_title, page_slug, parent_path=None):
    # create a new page and set it as the child of an existing page
    # return list of route paths
    # get the root of the current site
    site_model = apps.get_model('wagtailcore', 'Site')
    site = site_model.objects.get(is_default_site=True)
    root = site.root_page
    # since parent was not provided, make root
    parent = root
    # if a parent path is provided, use that as parent
    if parent_path:
        path_components = [component for component in parent_path.split('/') if component]

        try:
            route = root.route(None, path_components)
        except Http404:
            print("skipping page creation")

        parent = route.page

    # create page, add it as a child of parent, save, and publish
    new_page = SublandingPage(title=page_title, slug=page_slug)
    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")

    # return path
    return new_page.get_url(None, site)

def create_browse_page(page_title, page_slug, parent_path=None):
    # create a new page and set it as the child of an existing page
    # return list of route paths
    # get the root of the current site
    site_model = apps.get_model('wagtailcore', 'Site')
    site = site_model.objects.get(is_default_site=True)
    root = site.root_page
    # since parent was not provided, make root
    parent = root
    # if a parent path is provided, use that as parent
    if parent_path:
        path_components = [component for component in parent_path.split('/') if component]

        try:
            route = root.route(None, path_components)
        except Http404:
            print("skipping page creation")

        parent = route.page

    # create page, add it as a child of parent, save, and publish
    new_page = BrowsePage(title=page_title, slug=page_slug)
    try:
        parent.add_child(instance=new_page)
        new_page.save_revision().publish()
    except ValidationError:
        print("skipping page creation")

    # return path
    return new_page.get_url(None, site)
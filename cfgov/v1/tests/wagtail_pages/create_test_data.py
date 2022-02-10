import json

from django.db import IntegrityError

from v1.tests.wagtail_pages.helpers import (
    create_landing_page,
    create_sublanding_filterable_page,
    create_blog_page,
)
from mega_menu.models import Menu

def create_blog():
    REQUIRED_BLOG_PAGES = 101
    # create landing page as child of root
    landing_page_url = create_landing_page("About us", "about-us")

    # create sublanding page as child of landing page
    if landing_page_url and "/about-us" in landing_page_url:
        sublanding_page_url = create_sublanding_filterable_page("Blog", "blog", landing_page_url)

        # create blog pages as children of sublanding page
        if sublanding_page_url and "/about-us/blog" in sublanding_page_url:
            for i in range(REQUIRED_BLOG_PAGES):
                create_blog_page(str(i), str(i), sublanding_page_url)

def create_mega_menu_en():
    # remove previous mega menu objects and create new test data
    try:
        Menu.objects.all().delete()
        Menu.objects.create(language='en', submenus=json.dumps([
            {'type': 'submenu', 'value': {
                'title': 'Test Content',
                'columns': [{
                    'links': [
                        {'text': 'Home', 'url': '/'},
                        {'text': 'Still Home', 'url': '/'},
                    ]
                }]
            }},
            {'type': 'submenu', 'value': {
                'title': 'Test Content 2',
                'columns': [{
                    'links': [
                        {'text': 'Home', 'url': '/'},
                        {'text': 'Still Home', 'url': '/'},
                    ]
                }]
            }},
        ]))
    # if there was an error removing old data or new data can't be resolved.
    except IntegrityError:
        print("skipping en mega menu creation")
        return


create_blog()
create_mega_menu_en()
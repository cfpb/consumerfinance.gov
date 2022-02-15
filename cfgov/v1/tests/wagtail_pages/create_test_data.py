# This is a standalone file. Running it will create pages and a mega menu
# Categories and tags will still need to be populated manually
# This data allows integration tests to pass
# To run this file locally, run the following commands on a bash shell within
# the python container from the root folder:
#
# ./cfgov/manage.py shell
# exec(open('/src/consumerfinance.gov/cfgov/v1/tests/wagtail_pages/create_test_data.py').read())

from datetime import datetime
import json

from django.db import IntegrityError
from cfgov.v1.tests.wagtail_pages.helpers import create_browse_page

from v1.tests.wagtail_pages.helpers import (
    create_landing_page,
    create_sublanding_filterable_page,
    create_blog_page,
    create_browse_filterable_page,
    create_learn_page,
    create_sublanding_page,
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

def create_test_specific_blog_posts():
    # specific blog information needed to populate tests
    BLOG_PATH = "/about-us/blog/"
    LANGUAGE_TAG_ES = 'es'
    REQUIRED_NAME_ES = 'Estafas con beneficios'
    SLUG_ES = 'estafas-con-beneficios'
    SECOND_NAME_ES = 'Qué necesita saber sobre'
    SECOND_SLUG_ES = 'que-necesita-saber-sobre'
    LANGUAGE_TAG_TL = 'tl'
    REQUIRED_NAME_TL = 'Paano tutulungan'
    SLUG_TL = 'paano-tutulungan'
    REQUIRED_NAME_EN = 'Summary of the 2021'
    SLUG_EN = 'summary-of-the-2021'
    SECOND_NAME_EN = 'loans'
    SECOND_SLUG_EN = 'loans'
    THIRD_NAME_EN = 'student financial policy'
    THIRD_SLUG_EN = 'student-financial-policy'
    FOURTH_NAME_EN = 'consumer loans for consumers'
    FOURTH_SLUG_EN = 'consumer-loans-consumers'
    VALID_DATE = datetime(2020, 1, 1)
    OLDER_DATE = datetime(2019, 1, 1)
    NEWER_DATE = datetime(2021, 1, 1)
    # create pages with custom creation dates
    create_blog_page(REQUIRED_NAME_ES, SLUG_ES, BLOG_PATH, LANGUAGE_TAG_ES, VALID_DATE)
    create_blog_page(SECOND_NAME_ES, SECOND_SLUG_ES, BLOG_PATH, LANGUAGE_TAG_ES, VALID_DATE)
    create_blog_page(REQUIRED_NAME_TL, SLUG_TL, BLOG_PATH, LANGUAGE_TAG_TL, VALID_DATE)
    create_blog_page(REQUIRED_NAME_EN, SLUG_EN, BLOG_PATH, None, NEWER_DATE)
    create_blog_page(SECOND_NAME_EN, SECOND_SLUG_EN, BLOG_PATH, None, OLDER_DATE)
    create_blog_page(THIRD_NAME_EN, THIRD_SLUG_EN, BLOG_PATH, None, VALID_DATE)
    create_blog_page(FOURTH_NAME_EN, FOURTH_SLUG_EN, BLOG_PATH, None, VALID_DATE)

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

def create_learn_pages():
    VALID_DATE = datetime(2020, 1, 1)
    # create landing page as child of root
    landing_page_url = create_landing_page("Data Research", "data-research")

    # create sublanding page as child of landing page
    if landing_page_url and "/data-research" in landing_page_url:
        filterable_page_url = create_browse_filterable_page("Research Reports", "research-reports", landing_page_url)

        # create blog pages as children of sublanding page
        if filterable_page_url and "/data-research/research-reports" in filterable_page_url:
            create_learn_page("Report1", "report1", filterable_page_url, VALID_DATE)

        # create sublanding page
        sublanding_page_url = create_sublanding_page("Consumer Credit Trends", "consumer-credit-trends", landing_page_url)

        # create another filterable page
        if sublanding_page_url and "/data-research/consumer-credit-trends" in sublanding_page_url:
            filterable_page_url = create_browse_filterable_page("Auto Loans", "auto-loans", sublanding_page_url)

            # create brose page
            if filterable_page_url and "/data-research/consumer-credit-trends/auto-loans" in filterable_page_url:
                create_browse_page("Origination Activity", "origination-activity", filterable_page_url)


def create_feedback_pages():
    # create landing page as child of root
    landing_page_url = create_landing_page("Owning A Home", "owning-a-home")

    # create sublanding page as child of landing page
    if landing_page_url and "/owning-a-home" in landing_page_url:
        create_sublanding_page("Feedback", "feedback", landing_page_url)

def create_email_signup():
    # create landing page as child of root
    create_landing_page("Consumer Tools", "consumer-tools")


create_blog()
create_test_specific_blog_posts()
create_learn_pages()
create_feedback_pages()
create_email_signup()
create_mega_menu_en()
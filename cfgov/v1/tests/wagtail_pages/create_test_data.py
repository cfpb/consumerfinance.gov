from v1.tests.wagtail_pages.helpers import (
    create_landing_page,
    create_sublanding_filterable_page,
    create_blog_page,
)

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

create_blog()
import re
from bs4 import BeautifulSoup
from urlparse import urlsplit, urlunsplit
from django.conf import settings

replacements = (('/blog/', '/about-us/blog/'),
                ('/pressrelease/','/about-us/newsroom/'),
                ('/speeches/','/about-us/newsroom/'),
                ('/newsroom/','/about-us/newsroom/'),
                )

def update_path(path):
    for pattern, substitute in replacements:
        if path.startswith(pattern):
            new_path = path.replace(pattern,substitute)
            return new_path
    return path

def fix_link(link):
    urldata = urlsplit(link['href'])
    if urldata.scheme in ('http','https',''):
        # the empty string captures URL's without a scheme, like '/about-us'
        new_path = update_path(urldata.path)
        new_href = urlunsplit((None, None, urldata.path, urldata.query,
                              urldata.fragment))
        link['href'] = new_href
    else:
        return link

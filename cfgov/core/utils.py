import os
import re

from django.conf import settings
from django.core.signing import Signer
from django.core.urlresolvers import reverse

from bs4 import BeautifulSoup, NavigableString
from six.moves.urllib.parse import parse_qs, urlencode, urlparse

from core.templatetags.svg_icon import svg_icon

EXTERNAL_LINK_PATTERN = re.compile(settings.EXTERNAL_LINK_PATTERN)
NONCFPB_LINK_PATTERN = re.compile(settings.NONCFPB_LINK_PATTERN)
FILES_LINK_PATTERN = re.compile(settings.FILES_LINK_PATTERN)
DOWNLOAD_LINK_PATTERN = re.compile(settings.DOWNLOAD_LINK_PATTERN)
LINK_ICON_CLASSES = os.environ.get('LINK_ICON_CLASSES',
                                   'a-link a-link__icon')
LINK_ICON_TEXT_CLASSES = os.environ.get('LINK_ICON_TEXT_CLASSES',
                                        'a-link_text')


def append_query_args_to_url(base_url, args_dict):
    return "{0}?{1}".format(base_url, urlencode(args_dict))


def sign_url(url, secret=None):
    if secret:
        signer = Signer(secret, sep='||')
    else:
        signer = Signer(sep='||')

    url, signature = signer.sign(url).split('||')
    return (url, signature)


def signed_redirect(url):
    url, signature = sign_url(url)
    query_args = {'ext_url': url,
                  'signature': signature}

    return ('{0}?{1}'.format(reverse('external-site'), urlencode(query_args)))


def unsigned_redirect(url):
    query_args = {'ext_url': url}
    return ('{0}?{1}'.format(reverse('external-site'), urlencode(query_args)))


def extract_answers_from_request(request):
    answers = [(param.split('_')[1], value) for param, value in
               request.POST.items() if param.startswith('questionid')]
    return sorted(answers)


def format_file_size(bytecount, suffix='B'):
    """Convert a byte count into a rounded human-friendly file size."""
    for unit in ['', 'K', 'M', 'G']:
        if abs(bytecount) < 1024.0:
            return "{:1.0f} {}{}".format(bytecount, unit, suffix)
        bytecount /= 1024.0
    return "{:.0f} {}{}".format(bytecount, 'T', suffix)


def parse_links(html):
    soup = BeautifulSoup(html, 'html.parser')

    # This removes style tags <style>
    for s in soup('style'):
        s.decompose()

    # This removes all inline style attr's
    for tag in soup.recursiveChildGenerator():
        try:
            del tag['style']
        except TypeError:
            # 'NavigableString' object has does not have attr's
            pass

    # This adds the link markup
    link_tags = get_link_tags(soup)
    add_link_markup(link_tags)
    return soup.prettify()


def get_link_tags(soup):
    tags = []
    for a in soup.find_all('a', href=True):
        if not is_image_tag(a):
            tags.append(a)
    return tags


def is_image_tag(tag):
    for child in tag.children:
        if child.name in ['img', 'svg']:
            return True
    return False


def add_link_markup(tags):
    for tag in tags:
        icon = False
        if not tag.attrs.get('class', None):
            tag.attrs.update({'class': []})
        if tag['href'].startswith('/external-site/?'):
            # Sets the icon to indicate you're leaving consumerfinance.gov
            icon = 'external-link'
            components = urlparse(tag['href'])
            arguments = parse_qs(components.query)
            if 'ext_url' in arguments:
                external_url = arguments['ext_url'][0]
                tag['href'] = signed_redirect(external_url)

        elif NONCFPB_LINK_PATTERN.match(tag['href']):
            # Sets the icon to indicate you're leaving consumerfinance.gov
            icon = 'external-link'
            if EXTERNAL_LINK_PATTERN.match(tag['href']):
                tag['href'] = signed_redirect(tag['href'])
        elif DOWNLOAD_LINK_PATTERN.search(tag['href']):
            # Sets the icon to indicate you're downloading a file
            icon = 'download'
        if icon:
            tag.attrs['class'].append(LINK_ICON_CLASSES)
            # Wraps the link text in a span that provides the underline
            contents = tag.contents
            span = BeautifulSoup('', 'html.parser').new_tag('span')
            span['class'] = LINK_ICON_TEXT_CLASSES
            span.contents = contents
            tag.contents = [span, NavigableString(' ')]
            # Appends the SVG icon
            tag.contents.append(BeautifulSoup(svg_icon(icon), 'html.parser'))


class NoMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return 'nomigrations'

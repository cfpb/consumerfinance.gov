import re
from urllib.parse import parse_qs, urlencode, urlparse

from django.core.signing import Signer
from django.template.defaultfilters import slugify
from django.urls import reverse

from bs4 import BeautifulSoup

from core.templatetags.svg_icon import svg_icon


NON_GOV_LINKS = re.compile(
    r'https?:\/\/(?:www\.)?(?![^\?]+gov)(?!(content\.)?localhost).*'
)
NON_CFPB_LINKS = re.compile(
    r'(https?:\/\/(?:www\.)?(?![^\?]*(cfpb|consumerfinance).gov)'
    r'(?!(content\.)?localhost).*)'
)
DOWNLOAD_LINKS = re.compile(
    r'(?i)(\.pdf|\.doc|\.docx|\.xls|\.xlsx|\.csv|\.zip)$'
)
LINK_ICON_CLASSES = ['a-link', 'a-link__icon']

LINK_ICON_TEXT_CLASSES = ['a-link_text']

# Regular expression format string that will match any tag <tag_name> (that is
# not self-closing) and group its contents.
TAG_RE = (
    # Match an <tag_name[ attributes]>. If tag_name is not followed by a space
    # and any characters except >, it must be followed by >.
    r'<{tag_name}(?:\s+[^>]*?|)>'
    # And match everything inside before the closing </tag>
    r'.+?(?=</{tag_name}>)'
    # Then match the closing </tag>
    r'</{tag_name}>'
    # Make '.' match new lines, ignore case
    r'(?s)(?i)'
)

# Match <body…>…</body>
BODY_TAG_RE = re.compile(TAG_RE.format(tag_name="body"))

# Match <a…>…</a>
A_TAG_RE = re.compile(TAG_RE.format(tag_name="a"))

# If a link contains these elements, it should *not* get an icon
ICONLESS_LINK_CHILD_ELEMENTS = [
    'img', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
]


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

    return ("{0}?{1}".format(reverse("external-site"), urlencode(query_args)))


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


def get_body_html(html):
    body_match = BODY_TAG_RE.search(html)
    if body_match is not None:
        return body_match.group(0)


def get_link_tags(html):
    return A_TAG_RE.findall(html)


def add_link_markup(tag, request_path):
    """Add necessary markup to the given link and return if modified.

    Add an external link icon if the input is not a CFPB (internal) link.
    Add an external link redirect if the input is not a gov link.
    If it contains a descendent that should not get an icon, return the link.
    If not, add a download icon if the input is a file.
    Otherwise (internal link that is not a file), return None.
    """
    icon = False

    soup = BeautifulSoup(tag, 'html.parser')
    tag = soup.find('a', href=True)

    if tag is None:
        return None

    class_attrs = tag.attrs.setdefault('class', [])

    if request_path is not None:
        # Strips the path of the current page from hrefs that are internal page
        # anchor links.
        # TODO: Remove that functionality when we get to Wagtail>=2.7, which
        # adds the ability to create anchor links.
        in_page_anchor_pattern = request_path + '#'
        if tag['href'].startswith(in_page_anchor_pattern):
            # Strip current path from in-page anchor links
            tag['href'] = tag['href'].replace(request_path, '')
            return str(tag)

    if tag['href'].startswith('/external-site/?'):
        # Sets the icon to indicate you're leaving consumerfinance.gov
        icon = 'external-link'
        components = urlparse(tag['href'])
        arguments = parse_qs(components.query)
        if 'ext_url' in arguments:
            external_url = arguments['ext_url'][0]
            # Add original URL for print styles
            tag['data-orig-href'] = external_url
            # Add the redirect notice as well
            tag['href'] = signed_redirect(external_url)

    elif NON_CFPB_LINKS.match(tag['href']):
        # Sets the icon to indicate you're leaving consumerfinance.gov
        icon = 'external-link'
        if NON_GOV_LINKS.match(tag['href']):
            # Add original URL for print styles
            tag['data-orig-href'] = tag['href']
            # Add the redirect notice as well
            tag['href'] = signed_redirect(tag['href'])

    elif DOWNLOAD_LINKS.search(tag['href']):
        # Sets the icon to indicate you're downloading a file
        icon = 'download'

    # If the tag already ends in an SVG, we never want to append an icon.
    # If it has one or more SVGs but other content comes after them, we still
    # want to add one.
    svgs = tag.find_all('svg')
    if svgs:
        last_svg = svgs[-1]
        if not any(
            str(sibling or '').strip()
            for sibling in last_svg.next_siblings
        ):
            return str(tag)

    if tag.select(', '.join(ICONLESS_LINK_CHILD_ELEMENTS)):
        # If this tag has any children that are in our list of child elements
        # that should not get an icon, it doesn't get the icon. It might still
        # be an external link and modified accordingly above.
        return str(tag)

    if not icon:
        return None

    # We have an icon to append.
    for cls in LINK_ICON_CLASSES:
        if cls not in class_attrs:
            class_attrs.append(cls)

    icon_classes = {'class': LINK_ICON_TEXT_CLASSES}
    spans = tag.findAll('span', icon_classes)

    if spans:
        span = spans[-1]
    else:
        span = soup.new_tag('span', **icon_classes)
        span.contents = list(tag.contents)

        tag.clear()
        tag.append(span)

    span.insert_after(BeautifulSoup(' ' + svg_icon(icon), 'html.parser'))

    return str(tag)


def slugify_unique(context, value):
    """Generates a slug, making it unique for a context, if possible.

    If the context has a request object, the generated slug will be unique:

    >>> context = {'request': request}
    >>> slugify_unique(context, 'Some text')
    'some-text'
    >>> slugify_unique(context, 'Some text')
    'some-text-1'
    >>> slugify_unique(context, 'Some text')
    'some-text-2'

    This functionality is not thread safe.

    If the context lacks a request, this function falls back to the default
    behavior of Django slugify:

    https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.text.slugify

    >>> context = {}
    >>> slugify_unique(context, 'Some text')
    'some-text'
    >>> slugify_unique(context, 'Some text')
    'some-text'
    """
    slug = slugify(value)

    request = context.get('request')

    if request:
        attribute_name = '__slugify_unique_slugs'

        if not hasattr(request, attribute_name):
            setattr(request, attribute_name, list())

        used_slugs = getattr(request, attribute_name)

        original_slug = slug
        index = 1

        while slug in used_slugs:
            slug = '%s-%d' % (original_slug, index)
            index += 1

        used_slugs.append(slug)

    return slug

import re
from urllib.parse import parse_qs, urlencode, urlparse

from django.core.signing import Signer
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from bs4 import BeautifulSoup, NavigableString

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
LINK_ICON_CLASSES = 'a-link a-link__icon'

LINK_ICON_TEXT_CLASSES = 'a-link_text'

# Regular expression to match <a> links in HTML strings
A_TAG = re.compile(
    # Match an <a containing any attributes
    r'<a [^>]*?>'
    # And match everything inside before the closing </a>
    r'.+?(?=</a>)'
    # Then match the closing </a>
    r'</a>'
    # Make '.' match new lines, ignore case
    r'(?s)(?i)'
)

# If a link contains these elements, it should *not* get an icon
ICONLESS_LINK_CHILD_ELEMENTS = [
    'img', 'svg', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
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


def get_link_tags(html):
    return A_TAG.findall(html)


def add_link_markup(tag):
    """Add necessary markup to the given link and return if modified.

    Add an external link icon if the input is not a CFPB (internal) link.
    Add an external link redirect if the input is not a gov link.
    If it contains a descendent that should not get an icon, return the link.
    If not, add a download icon if the input is a file.
    Otherwise (internal link that is not a file), return None.
    """
    icon = False

    tag = BeautifulSoup(tag, 'html.parser').find('a', href=True)

    if tag is None:
        return None

    if not tag.attrs.get('class', None):
        tag.attrs.update({'class': []})

    if tag['href'].startswith('/external-site/?'):
        # Sets the icon to indicate you're leaving consumerfinance.gov
        icon = 'external-link'
        components = urlparse(tag['href'])
        arguments = parse_qs(components.query)
        if 'ext_url' in arguments:
            external_url = arguments['ext_url'][0]
            # Add the redirect notice as well
            tag['href'] = signed_redirect(external_url)

    elif NON_CFPB_LINKS.match(tag['href']):
        # Sets the icon to indicate you're leaving consumerfinance.gov
        icon = 'external-link'
        if NON_GOV_LINKS.match(tag['href']):
            # Add the redirect notice as well
            tag['href'] = signed_redirect(tag['href'])

    elif DOWNLOAD_LINKS.search(tag['href']):
        # Sets the icon to indicate you're downloading a file
        icon = 'download'

    if tag.select(', '.join(ICONLESS_LINK_CHILD_ELEMENTS)):
        # If this tag has any children that are in our list of child elements
        # that should not get an icon, it doesn't get the icon. It might still
        # be an external link and modified accordingly above.
        return str(tag)

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
        return str(tag)

    return None


class NoMigrations(object):
    """Class to disable app migrations through settings.MIGRATION_MODULES.

    The MIGRATION_MODULES setting can be used to tell Django where to look
    for an app's migrations (by default this is the "migrations" subdirectory).
    This class simulates a dictionary where a lookup for any app returns a
    value that causes Django to think that no migrations exist.
    """
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


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

    https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.text.slugify

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

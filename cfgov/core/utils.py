import re

from django.template.defaultfilters import slugify

from bs4 import BeautifulSoup, NavigableString

from core.templatetags.svg_icon import svg_icon


NON_CFPB_LINKS = re.compile(
    # HTTP or HTTPS
    r"https?:\/\/"
    # Negative lookahead: don't match anything that matches what follows
    r"(?!"
    # Match any subdomains
    r"((\w+\.)*"
    # Match consumerfinance.gov, cfpb.gov, or localhost
    r"(consumerfinance\.gov|cfpb\.gov|localhost))"
    # Match a port number, if provided
    r"(?:\:\d+)?"
    # Match the rest of the URL
    r".*)"
)

LINK_PATTERN = re.compile(
    r"^(?P<schema>https?)://(?P<domain>[^/:]+):?(?P<port>\d+)?(?P<path>/?.*)?$"
)

DOWNLOAD_LINKS = re.compile(
    r"(?i)(\.pdf|\.doc|\.docx|\.xls|\.xlsx|\.csv|\.zip)$"
)
ASK_CFPB_LINKS = re.compile(
    # https://regexr.com/5opro
    r"(https?:\/\/(www\.)?(cfpb|consumerfinance)\.gov)?\/ask\-cfpb\/([-\w]{1,244})-(en)-(?P<ask_id>\d{1,6})\/?$"  # noqa: E501
)

LINK_ICON_CLASSES = ["a-link"]

LINK_ICON_TEXT_CLASSES = ["a-link__text"]

# Regular expression format string that will match any tag <tag_name> (that is
# not self-closing) and group its contents.
TAG_RE = (
    # Match an <tag_name[ attributes]>. If tag_name is not followed by a space
    # and any characters except >, it must be followed by >.
    r"<{tag_name}(?:\s+[^>]*?|)>"
    # And match everything inside before the closing </tag>
    r".+?(?=</{tag_name}>)"
    # Then match the closing </tag>
    r"</{tag_name}>"
    # Make '.' match new lines, ignore case
    r"(?s)(?i)"
)

# Match <body…>…</body>
BODY_TAG_RE = re.compile(TAG_RE.format(tag_name="body"))

# Match <a…>…</a>
A_TAG_RE = re.compile(TAG_RE.format(tag_name="a"))

# If a link contains these elements, it should *not* get an icon
ICONLESS_LINK_CHILD_ELEMENTS = [
    "img",
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
]


def ask_short_url(url):
    match = ASK_CFPB_LINKS.search(url)
    ask_id = match.groupdict().get("ask_id")
    return f"cfpb.gov/askcfpb/{ask_id}"


def extract_answers_from_request(request):
    answers = [
        (param.split("_")[1], value)
        for param, value in request.POST.items()
        if param.startswith("questionid")
    ]
    return sorted(answers)


def format_file_size(bytecount, suffix="B"):
    """Convert a byte count into a rounded human-friendly file size."""
    for unit in ["", "K", "M", "G"]:
        if abs(bytecount) < 1024.0:
            return f"{bytecount:1.0f} {unit}{suffix}"
        bytecount /= 1024.0
    return "{:.0f} {}{}".format(bytecount, "T", suffix)


def get_body_html(html):
    body_match = BODY_TAG_RE.search(html)
    if body_match is not None:
        return body_match.group(0)


def get_link_tags(html):
    return A_TAG_RE.findall(html)


def add_link_markup(tag, request_path):
    """Add necessary markup to the given link and return if modified.

    If it's a jump link, return the tag with the page's path removed.
    If it's an Ask CFPB link, return the tag with the shortened Ask URL.
    If it's an external link, add an external-link icon.
    If it's a non-CFPB govt link, add an external-link icon.
    If it contains a descendent that should not get an icon, return the link.
    If not, add a download icon if the input is a file.
    Otherwise (internal link that is not a file), return None.
    """
    icon = False

    soup = BeautifulSoup(tag, "html.parser")
    tag = soup.find("a", href=True)

    if tag is None:
        return None

    href = tag["href"]
    class_attrs = tag.attrs.setdefault("class", [])

    if request_path is not None:
        # Strips the path of the current page from hrefs that are internal page
        # anchor links.
        # TODO: Remove that functionality when we get to Wagtail>=2.7, which
        # adds the ability to create anchor links.
        in_page_anchor_pattern = request_path + "#"
        if tag["href"].startswith(in_page_anchor_pattern):
            # Strip current path from in-page anchor links
            tag["href"] = href.replace(request_path, "")
            return str(tag)

    if ASK_CFPB_LINKS.match(href):
        # Use short URL when printing Ask CFPB links
        tag["data-pretty-href"] = ask_short_url(href)
        return str(tag)

    if NON_CFPB_LINKS.match(href):
        # Sets the icon to indicate you're leaving consumerfinance.gov
        icon = "external-link"

    elif DOWNLOAD_LINKS.search(href):
        # Sets the icon to indicate you're downloading a file
        icon = "download"

    # If the tag already ends in an SVG, we never want to append an icon.
    # If it has one or more SVGs but other content comes after them, we still
    # want to add one.
    svgs = tag.find_all("svg")
    if svgs:
        last_svg = svgs[-1]
        if not any(
            str(sibling or "").strip() for sibling in last_svg.next_siblings
        ):
            return str(tag)

    if tag.select(", ".join(ICONLESS_LINK_CHILD_ELEMENTS)):
        # If this tag has any children that are in our list of child elements
        # that should not get an icon, it doesn't get the icon. It might still
        # be an external link and modified accordingly above.
        return str(tag)

    if not icon:
        return

    icon_classes = {"class": LINK_ICON_TEXT_CLASSES}
    spans = tag.findAll("span", icon_classes)

    icon_soup = BeautifulSoup(svg_icon(icon), "html.parser")

    # If this is an <a class="a-btn"> tag without a span inside, we want to
    # add proper markup so that the link appears as a button with the icon on
    # the right side.
    if not spans and "a-btn" in class_attrs:
        span = soup.new_tag("span")
        # Set the span's contents to whatever is in the `<a>` currently
        span.contents = list(tag.contents)
        # Remove that stuff from the `<a>`
        tag.clear()
        # Add the span back in
        tag.append(span)
        tag.contents.append(icon_soup)

    # Otherwise, either modify an existing <span> or add a new one so that
    # it has the proper non-button link classes, and then add the icon after
    # the span.
    else:
        # Since we're adding an icon, also add class="a-link" to
        # the <a> tag. We don't do this if the link is a button.
        for cls in LINK_ICON_CLASSES:
            if cls not in class_attrs:
                class_attrs.append(cls)

        if spans:
            span = spans[-1]
        else:
            span = soup.new_tag("span", **icon_classes)
            span.contents = list(tag.contents)

            tag.clear()
            tag.append(span)

        # Whether we used an existing text span with a-link__text or added a
        # new one, we want to make sure that the link text doesn't include any
        # wrapping whitespace, otherwise it'll be incorrectly underlined.
        #
        # This fixes tags like <a> text with surrounding whitespace </a> or
        # tags like <a> text with <strong>other</strong> tag </a> but not tags
        # like <a> text with <strong>other tag with whitespace </strong></a>.
        if span.contents:
            if isinstance(span.contents[0], NavigableString):
                span.contents[0] = NavigableString(span.contents[0].lstrip())
            if isinstance(span.contents[-1], NavigableString):
                span.contents[-1] = NavigableString(span.contents[-1].rstrip())

        tag.append(" ")
        tag.append(icon_soup)

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

    request = context.get("request")

    if request:
        attribute_name = "__slugify_unique_slugs"

        if not hasattr(request, attribute_name):
            setattr(request, attribute_name, list())

        used_slugs = getattr(request, attribute_name)

        original_slug = slug
        index = 1

        while slug in used_slugs:
            slug = f"{original_slug}-{index}"
            index += 1

        used_slugs.append(slug)

    return slug

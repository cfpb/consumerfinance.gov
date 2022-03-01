import re

from django.conf import settings

from regdown import extract_labeled_paragraph

from regulations3k.models import Section


DEFAULT_REGULATIONS_REFERENCE_MAPPING = [
    (r"(?P<section>[\w]+)-(?P<paragraph>[\w-]*)", "{section}", "{paragraph}"),
]


def resolve_reference(reference):
    """Given a reference, return destination section and paragraph labels
    This function uses the REGULATIONS_REFERENCE_MAPPING setting to resolve
    references into their destination section and paragraph labels. It does
    not containing that reference"""
    reference_mapping = getattr(
        settings,
        "REGULATIONS_REFERENCE_MAPPING",
        DEFAULT_REGULATIONS_REFERENCE_MAPPING,
    )

    for reference_map in reference_mapping:
        reference_re = re.compile(reference_map[0])
        match = reference_re.match(reference)
        if match:
            dest_section_label = reference_map[1].format(**match.groupdict())
            dest_paragraph_label = reference_map[2].format(**match.groupdict())
            return (dest_section_label, dest_paragraph_label)

    return (None, None)


def get_contents_resolver(effective_version):
    """Return a Regdown contents_resolver function for the RegulationPage
    This constructs a contents_resolver that will resolve references and
    return their contents for all sections that are part of the current
    EffectiveVersion served by the given page."""
    section_query = Section.objects.filter(subpart__version=effective_version)

    def contents_resolver(reference):
        dest_section_label, dest_paragraph_label = resolve_reference(reference)
        try:
            dest_section = section_query.get(label=dest_section_label)
        except Section.DoesNotExist:
            return ""
        dest_paragraph = extract_labeled_paragraph(
            dest_paragraph_label, dest_section.contents, exact=False
        )
        return dest_paragraph

    return contents_resolver


def get_url_resolver(page, date_str=None):
    """Returns a Regdown url_resolver function for the RegulationPage
    This constructs a url_resolver that will resolve the URL of references to
    any section that is part of the current EffectiveVersion served by the
    given page."""

    section_kwargs = {}
    if date_str is not None:
        section_kwargs["date_str"] = date_str

    def url_resolver(reference):
        dest_section_label, dest_paragraph_label = resolve_reference(reference)
        section_kwargs["section_label"] = dest_section_label
        return "{page_url}{section_url}#{paragraph_label}".format(
            page_url=page.url,
            section_url=page.reverse_subpage("section", kwargs=section_kwargs).lower(),
            paragraph_label=dest_paragraph_label,
        )

    return url_resolver

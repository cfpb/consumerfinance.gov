# -*- coding: utf-8 -*-

import logging
import re

from regulations3k.models import Part, Section
from regulations3k.scripts.ecfr_importer import PART_ALLOWLIST

REG_BASE = "/rules-policy/regulations/{}/"
SECTION_RE = re.compile(r"(?:§|Section|12 CFR)\W+([^\s]+)")
PARTS_RE = re.compile(
    r"(?P<part>\d{4})[.-](?P<section>[0-9A-Z]+)(?P<ids>\([a-zA-Z0-9)(]+)?"
)
ID_RE = re.compile(r"\(([a-zA-Z0-9]{1,4})\)")

logger = logging.getLogger(__name__)


def get_url(section_reference):
    if not PARTS_RE.match(section_reference):
        return
    parts = PARTS_RE.match(section_reference).groupdict()
    part = parts.get("part")
    if part not in PART_ALLOWLIST:
        return
    part_url = REG_BASE.format(part)
    section_url = "{}{}/".format(part_url, parts.get("section"))
    if not parts.get("ids"):
        return section_url
    paragraph_id = "-".join(ID_RE.findall(parts.get("ids")))
    if paragraph_id:
        return "{}#{}".format(section_url, paragraph_id)
    else:
        return section_url


def insert_section_links(regdown):
    """Turn internal section references into links."""
    section_refs = SECTION_RE.findall(regdown)
    if not section_refs:
        return
    index_head = 0
    for i, ref in enumerate(section_refs):
        url = get_url(ref)
        if url:
            link = '<a href="{}" data-linktag="{}">{}</a> '.format(url, i, ref)
            regdown = regdown[:index_head] + regdown[index_head:].replace(
                ref, link, 1
            )
            index_head = regdown.index(link) + len(link)
    return regdown


def insert_links(reg=None):
    if reg is None:
        parts = Part.objects.all()
    else:
        parts = Part.objects.filter(part_number=reg)
    live_versions = [part.effective_version for part in parts]
    live_sections = Section.objects.filter(
        subpart__version__in=live_versions
    ).exclude(subpart__title__contains="Supplement I")
    for section in live_sections:
        if "data-linktag" in section.contents:
            logger.info("Section {} already has links applied".format(section))
            continue
        linked_regdown = insert_section_links(section.contents)
        if not linked_regdown:
            logger.info(
                "No section references found in section {}".format(section)
            )
            continue
        else:
            logger.info("Links added to section {}".format(section))
            section.contents = linked_regdown
            section.save()


def run(*args):
    if args:
        insert_links(reg=args[0])
    else:
        insert_links()

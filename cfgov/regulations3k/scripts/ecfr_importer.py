from __future__ import unicode_literals

import datetime
import logging
import re
import sys

# from bs4 import UnicodeDammit
import requests
from bs4 import BeautifulSoup as bS
from regulations3k.models.django import (
    EffectiveVersion, Part, Section, Subpart
)
from regulations3k.scripts.patterns import (  # dot_id_patterns,
    IdLevelState, paren_id_patterns, title_pattern
)


# TODO
# - Parse appendices
# - parse interps
# - insert interp refs
# ODDITIES TO HANDLE
# tables
# dash-forms (forms with dash-extended entry fields)
# gif graphics
# pdf graphics

logger = logging.getLogger(__name__)
# The latest ECFR version of title-12, updated every few days
CFR_TITLE = '12'
CFR_CHAPTER = 'X'
LATEST_ECFR = ("https://www.gpo.gov/fdsys/bulkdata/ECFR/"
               "title-{0}/ECFR-title{0}.xml".format(CFR_TITLE))


class PayLoad(object):
    """Container for regulation components."""

    part = None
    version = None
    subparts = {
        'section_subparts': [],
        'appendix_subpart': None,
        'interp_subpart': None,
    }
    sections = []
    appendices = []
    interpretations = []


PAYLOAD = PayLoad()
LEVEL_STATE = IdLevelState()


def parse_part(part_soup, part_number):
    part, created = Part.objects.get_or_create(
        part_number=part_number,
        chapter=CFR_CHAPTER,
        cfr_title_number=CFR_TITLE)
    if created:
        raw_title = part_soup.find('HEAD').text
        parsed_title = title_pattern.match(raw_title)
        part.title = parsed_title.group(2).title()
        part.letter_code = parsed_title.group(3).replace(
            'REGULATION', '').strip()
        part.save()
        logger.info("Created Part {}, {}".format(part_number, part.title))
    PAYLOAD.part = part
    return part


def parse_version(soup, part):
    auth = soup.find('AUTH').find('PSPACE').text.strip()
    source = soup.find('SOURCE').find('PSPACE').text.strip()
    version, created = EffectiveVersion.objects.get_or_create(
        acquired=datetime.date.today(),
        authority=auth,
        part=part,
        source=source,
    )
    if created:
        version.draft = True
        version.save()
        logger.info("Created new draft version for {}".format(part))
    PAYLOAD.version = version
    return version


def parse_subparts(part_soup, subpart_list, part):
    """Createa a mapping of subparts and the sections they contain."""
    _appendices, cr = Subpart.objects.get_or_create(
        title="Appendices",
        label="{}-Appendices".format(part.part_number),
        version=PAYLOAD.version)
    PAYLOAD.subparts['appendix_subpart'] = _appendices
    _interps, cr = Subpart.objects.get_or_create(
        title="Supplement I to Part {}".format(part.part_number),
        label="Official Interpretations",
        version=PAYLOAD.version)
    PAYLOAD.subparts['interp_subpart'] = _interps

    labeled_subparts = [subp for subp in subpart_list
                        if subp.find('HEAD').text.strip()]
    if not labeled_subparts:
        generic_subpart, cr = Subpart.objects.get_or_create(
            label=part.part_number,
            title="General",
            version=PAYLOAD.version
        )
        PAYLOAD.subparts['section_subparts'].append(generic_subpart)
        parse_sections(part_soup.find_all('DIV8'), part, generic_subpart)
    else:
        for element in labeled_subparts:
            _subpart, cr = Subpart.objects.get_or_create(
                title=element.find('HEAD').text.strip(),
                label=part.part_number,
                version=PAYLOAD.version
            )
            PAYLOAD.subparts['section_subparts'].append(_subpart)
            subpart_sections = element.find_all('DIV8')
            parse_sections(subpart_sections, part, _subpart)


def ital_to_bold(soup):
    """Replace initial italics clauses with markdown-style bolding"""
    if soup.find('I'):
        ital_content = soup.find('I').text
        soup.find('I').replaceWith('**{}** '.format(ital_content))
    return soup


def extract_id(text):
    match = re.search(paren_id_patterns['any'], text)
    if match:
        return re.search(paren_id_patterns['any'], text).group(1)


def extract_level_one_ids(text):
    """
    Extract up to three valid element IDS from an initial paragraph.
    """
    ids = re.findall(paren_id_patterns['initial'], text)[:3]
    if not ids:
        return
    if ids[0].islower():
        good_ids = 1
    else:
        return
    if len(ids) > 1 and ids[1] == '1':
        good_ids += 1
        if len(ids) == 3 and ids[2] == 'i':
            good_ids += 1

    return "-".join([pid for pid in ids[:good_ids]])


def parse_section_paragraphs(paragraph_soup):
    paragraph_content = ''
    for p in paragraph_soup:
        p = ital_to_bold(p)
        if LEVEL_STATE.level() == 1:
            new_pid = extract_level_one_ids(p.text) or ''
            if new_pid.count('-') > 0:
                LEVEL_STATE.current_id = new_pid
                pid = new_pid
            else:
                LEVEL_STATE.next_token = new_pid
                pid = LEVEL_STATE.next_id()
            if pid:
                paragraph_content += "\n{" + pid + "}\n"
        else:
            id_token = extract_id(p.text)
            if id_token:
                LEVEL_STATE.next_token = id_token
                pid = LEVEL_STATE.next_id()
                paragraph_content += "{" + pid + "}\n"
        paragraph_content += "{}\n\n".format(p.text.replace('\xc2', ''))
    return paragraph_content


def parse_sections(section_list, part, subpart):
    for section_element in section_list:
        section_content = parse_section_paragraphs(
            section_element.find_all('P'))
        section_number = section_element['N'].rsplit('.')[-1]
        _section = Section(
            subpart=subpart,
            label="{}-{}".format(part.part_number, section_number),
            title=section_element.find(
                'HEAD').text.strip().replace('\xc2', ''),
            contents=section_content
        )
        _section.save()
        # try:  # try-except clause for initial troubleshooting
        #     _section.save()
        # except Exception as e:
        #     LEVEL_STATE.section_error = section_content
        #     error_file = (
        #         "/Users/higginsw/Desktop/XML/section_error_{}-{}.txt".format(
        #             part.part_number, section_number))
        #     with open(error_file, 'a+') as f:
        #         f.write(section_content.encode('utf-8', 'replace'))
        #     print("Error saving section {}-{}:\n "
        #           "{}\n See {} for details".format(
        #               part.part_number,
        #               section_number,
        #               e,
        #               error_file))


def parse_appendices(appendices_list, part):
    """
    Parse the list of appendices, tease out interps and send them along,
    and then process the remaining appendices.
    """
    PAYLOAD.appendices = {}


def parse_interps(interp_list, part):
    """
    Take the remaining list of interpretations, break them down into
    individual section interpretations, and process them by subpart.
    """
    PAYLOAD.interpretations = {}


def ecfr_to_regdown(part_number, file_path=None):
    """
    Extract a regulation Part from eCFR XML, and create regdown content.

    The default XML source is the latest regulation posting at www.gpo.gov,
    which gets updated every few days.

    If `file_path` is specified, a local XML file is parsed instead.

    DIV1 is a title (as in Title 12)
    DIV3 is a chapter (not used here)
    DIV5 is a part
    DIV6 is a subpart
    DIV8 is a section
    DIV9 is an appendix
    DIV9 element whose HEAD starts with 'Supplement I' is an interpretation
    """
    starter = datetime.datetime.now()
    if file_path:
        try:
            with open(file_path, 'r') as f:
                markup = f.read()
        except IOError:
            logger.info("Could not open local file {}".format(file_path))
            return
    else:
        ecfr_request = requests.get(LATEST_ECFR)
        if ecfr_request.reason != 'OK':
            logger.info(
                "ECFR request failed with code {} and reason {}".format(
                    ecfr_request.status_code, ecfr_request.reason))
            return
        ecfr_request.encoding = 'utf-8'
        markup = ecfr_request.text
    soup = bS(markup, "lxml-xml")
    parts = soup.find_all('DIV5')
    try:
        part_soup = [div for div in parts if div['N'] == part_number][0]
    except IndexError:
        logger.info(
            "Regulation could not be found for part {}".format(part_number))
        return
    part = parse_part(part_soup, part_number)
    parse_version(part_soup, part)
    subpart_list = part_soup.find_all('DIV6')
    parse_subparts(part_soup, subpart_list, part)
    appendices_list = part_soup.find_all('DIV9')
    interps_list = [div for div in appendices_list
                    if div.find('HEAD').text.startswith('Supplement I')]
    parse_appendices(appendices_list, part)
    parse_interps(interps_list, part)

    msg = (
        "Draft version of Part {} created.\n"
        "Parsing took {}".format(
            part_number, (datetime.datetime.now() - starter))
    )
    return msg


def run(*args):
    if len(args) not in [1, 2]:
        logger.info(
            "Usage: ./cfgov/manage.py runscript "
            "ecfr_importer --script-args "
            "[PART NUMBER] [OPTIONAL XML FILE PATH]")
        sys.exit(1)
    elif len(args) == 1:
        ecfr_to_regdown(args[0])
    else:
        ecfr_to_regdown(args[0], file_path=args[1])

from __future__ import unicode_literals

import datetime
import logging
import re
import sys

import requests
from bs4 import BeautifulSoup as bS
from regulations3k.models.django import (
    EffectiveVersion, Part, Section, Subpart
)
from regulations3k.scripts.patterns import (  # dot_id_patterns,
    IdLevelState, paren_id_patterns, title_pattern
)
from regulations3k.scripts.roman import roman_to_int


# TODO
# - Parse appendices
# - parse interps
# - insert interp refs
# ODDITIES TO HANDLE
# tables
# gif graphics
# pdf graphics

logger = logging.getLogger(__name__)

# eCFR globals
CFR_TITLE = '12'
CFR_CHAPTER = 'X'
PART_WHITELIST = [
    '1002', '1003', '1004', '1005', '1010', '1011',
    '1012', '1013', '1024', '1026', '1030'
]
# The latest eCFR version of title-12, updated every few days
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


def pre_process_tags(soup):
    """
    Convert initial italics-tagged text to markdown bold
    and convert the rest to markdown italics.
    """
    if soup.find('I'):
        ital_content = soup.find('I').text
        soup.find('I').replaceWith('**{}**'.format(ital_content))
    for element in soup.find_all('I'):
        i_content = element.text
        element.replaceWith('*{}*'.format(i_content))
    return soup


def bold_first_italics(graph):
    """For a newly broken-up graph, convert the first italics text to bold."""
    if graph.count('*') > 1:
        return graph.replace('*', '**', 2)
    else:
        return graph


def combine_bolds(graph):
    """
    Make ID marker bold and remove redundant bold markup between bold elements.
    """
    if graph.startswith('('):
        graph = graph.replace(
            '  ', ' ').replace(
            '(', '**(', 1).replace(
            ')', ')**', 1).replace(
            '** **', ' ', 1)
    return graph


def graph_top(graph):
    "Weed out the common sources of errant IDs"
    return graph.partition(
        'paragraph')[0].partition(
        '12 CFR')[0].partition(
        '\xa7')[0][:200]


def parse_singleton_graph(graph):
    """Take a graph with a single ID and return styled with a braced ID"""
    new_graph = ''
    id_match = re.search(paren_id_patterns['initial'], graph_top(graph))
    if not id_match:
        return '\n' + combine_bolds(graph) + '\n'
    id_token = id_match.group(1).strip('*')
    if not token_validity_test(id_token):
        return '\n' + combine_bolds(graph) + '\n'
    LEVEL_STATE.next_token = id_token
    pid = LEVEL_STATE.next_id()
    new_graph += "\n{" + pid + "}\n"
    new_graph += combine_bolds(graph) + '\n'
    return new_graph


def token_validity_test(token):
    "Make sure a singleton token is some kind of valid ID."
    if (
            token.isdigit()
            or roman_to_int(token)
            or (token.isalpha() and len(token) == 1)
            or (token.isalpha() and len(token) == 2 and token[0] == token[1])):
        return True
    else:
        return False


def parse_multi_id_graph(graph, ids):
    """
    Parse a graph with 1 to 3 ids and return
    individual graphs with their own braced IDs.
    """
    new_graphs = ''
    LEVEL_STATE.next_token = ids[0]
    pid1 = LEVEL_STATE.next_id()
    split1 = graph.partition('({})'.format(ids[1]))
    text1 = combine_bolds(split1[0])
    pid2_marker = split1[1]
    remainder = bold_first_italics(split1[2])
    new_graphs += "\n{" + pid1 + "}\n"
    new_graphs += text1 + '\n'
    LEVEL_STATE.next_token = ids[1]
    pid2 = LEVEL_STATE.next_id()
    new_graphs += "\n{" + pid2 + "}\n"
    if len(ids) == 2:
        text2 = combine_bolds(" ".join([pid2_marker, remainder]))
        new_graphs += text2 + '\n'
        return new_graphs
    else:
        split2 = remainder.partition('({})'.format(ids[2]))
        pid3_marker = split2[1]
        remainder2 = bold_first_italics(split2[2])
        text2 = combine_bolds(" ".join([pid2_marker, split2[0]]))
        new_graphs += text2 + '\n'
        LEVEL_STATE.next_token = ids[2]
        pid3 = LEVEL_STATE.next_id()
        new_graphs += "\n{" + pid3 + "}\n"
        text3 = combine_bolds(" ".join([pid3_marker, remainder2]))
        new_graphs += text3 + '\n'
        return new_graphs


def roman_test(id_token):
    """
    Determine whether the root ID of a potential multi_ID paragraph is a roman
    numeral increment surfing levels 3 or 6 (the roman levels of a-1-i-A-1-i)
    """
    roman_int = roman_to_int(id_token)
    if not roman_int:
        return False
    if LEVEL_STATE.level() not in [3, 6]:
        return False
    if roman_int - 1 == roman_to_int(LEVEL_STATE.current_token()):
        return True


def multiple_id_test(ids):
    """
    Decide, based on the first two IDS,
    whether to proceed with multi-ID processing.

    Allowed multi-ID patterns are:
      (lowercase)(1) - and the lowercase cannot be a roman_numeral increment
      (digit)(i)
      (roman)(A)
      (uppercase)(1)
    """
    if len(ids) < 2:
        return
    root_token = ids[0]
    # levels 1 or 4
    if (root_token.isalpha()
            and len(root_token) < 3
            and not roman_test(root_token)
            and ids[1] == '1'):
        good_ids = 2
        if len(ids) == 3 and ids[2] == 'i':
            good_ids = 3
        return ids[:good_ids]
    # levels 2 or 5
    if root_token.isdigit() and ids[1] == 'i':
        good_ids = 2
        if len(ids) == 3 and ids[2] == 'A' and LEVEL_STATE.level() != 5:
            good_ids = 3
        return ids[:good_ids]
    # level 3
    if roman_to_int(root_token) and ids[1] == 'A':
        good_ids = 2
        if len(ids) == 3 and ids[2] == '1':
            good_ids = 3
        return ids[:good_ids]
    # multiples not allowed at level 6


def parse_ids(graph):
    """
    Extract up to three valid element IDs (indentaion markers)
    from a paragraph, and return a paragraph for each ID found.
    """
    raw_ids = re.findall(
        paren_id_patterns['initial'], graph_top(graph))
    clean_ids = [bit.strip('*') for bit in raw_ids if bit][:3]
    for clean_id in clean_ids:
        #  clean up edge-case bolding caused by italicized IDs, such as
        #  '(F)(<I>1</I>)' from reg 1026.7
        graph = graph.replace("**{}**".format(clean_id), clean_id)
    valid_ids = multiple_id_test(clean_ids)
    if not valid_ids or LEVEL_STATE.level() == 6:
        return parse_singleton_graph(graph)
    else:
        return parse_multi_id_graph(graph, valid_ids)


def parse_section_paragraphs(paragraph_soup):
    paragraph_content = ''
    for p in paragraph_soup:
        p = pre_process_tags(p)
        graph = p.text.replace('\n', '')
        paragraph_content += parse_ids(graph)
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

    To avoid mischief, we make sure the part number is on a whitelist.
    """
    if part_number not in PART_WHITELIST:
        raise ValueError('Provided Part number is not one we support.')
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
    part_soup = [div for div in parts if div['N'] == part_number][0]
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

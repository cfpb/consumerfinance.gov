from __future__ import unicode_literals

import datetime
import logging
import re
import sys

import requests
from bs4 import BeautifulSoup as bS
from dateutil import parser

from regulations3k.models.django import (
    EffectiveVersion, Part, Section, Subpart
)
from regulations3k.scripts.integer_conversion import int_to_alpha, roman_to_int
from regulations3k.scripts.patterns import (
    IdLevelState, dot_id_patterns, paren_id_patterns, title_pattern
)


# TODO
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
    '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009',
    '1010', '1011', '1012', '1013', '1014', '1015', '1016',
    '1022', '1024', '1025', '1026', '1030', '1041',
    '1070', '1071', '1072', '1073', '1074', '1075', '1076',
    '1080', '1081', '1082', '1083', '1090', '1091',
]
LEGACY_PARTS = [
    '1002', '1003', '1004', '1005', '1010', '1011', '1012', '1013',
    '1024', '1026', '1030',
]
# The latest eCFR version of title-12, updated every few days
LATEST_ECFR = ("https://www.gpo.gov/fdsys/bulkdata/ECFR/"
               "title-{0}/ECFR-title{0}.xml".format(CFR_TITLE))
FR_date_query = (
    "https://www.federalregister.gov/api/v1/documents.json?"
    "fields[]=effective_on&"
    "per_page=20&"
    "order=relevance&"
    "conditions[agencies][]=consumer-financial-protection-bureau&"
    "conditions[type][]=RULE&"
    "conditions[cfr][title]=12&"
    "conditions[cfr][part]={}"
)
HEADLINE_MAP = {
    'HD1': "\n## {}\n",
    'HD2': "\n### {}\n",
    'HD3': "\n#### {}\n",
}
LINK_FARM_TAGS = ['XREF', 'FP-1', 'FP-2']


def get_effective_date(part_number):
    today = datetime.date.today()
    FR_query = FR_date_query.format(part_number)
    FR_response = requests.get(FR_query)
    if not FR_response.ok or not FR_response.json():
        return
    FR_json = FR_response.json()
    date_strings = [result['effective_on'] for result in FR_json['results']]
    dates = sorted(set(
        [parser.parse(date).date() for date in date_strings if date]
    ))
    return [date for date in dates if date <= today][-1]


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
    effective_date = None


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
    version = EffectiveVersion(
        acquired=datetime.date.today(),
        effective_date=PAYLOAD.effective_date,
        authority=auth,
        part=part,
        source=source,
        draft=True,
    )
    version.save()
    PAYLOAD.version = version
    return version


def parse_subparts(part_soup, part):
    """
    Create subparts and the elements they contain.

    We need to parse appendices first so that, if there are interpretations,
    we have a mapping of interpretation references to insert into sections
    during section parsing.
    """
    subpart_list = part_soup.find_all('DIV6')
    appendix_subpart = Subpart(
        title="Appendices",
        label="{}-Appendices".format(part.part_number),
        version=PAYLOAD.version)
    appendix_subpart.save()
    PAYLOAD.subparts['appendix_subpart'] = appendix_subpart
    interp_subpart = Subpart(
        title="Supplement I to Part {} - Official Interpretations".format(
            part.part_number),
        label="{}-Interpretations".format(part.part_number),
        version=PAYLOAD.version)
    interp_subpart.save()
    PAYLOAD.subparts['interp_subpart'] = interp_subpart
    appendices = part_soup.find_all('DIV9')
    if appendices:
        if appendices[-1].find('HEAD').text.startswith('Supplement I'):
            interp_div = appendices.pop(-1)
            parse_interps(interp_div, part, PAYLOAD.subparts['interp_subpart'])
        parse_appendices(appendices, part)
    labeled_subparts = [subp for subp in subpart_list
                        if subp.find('HEAD').text.strip()]
    if not labeled_subparts:
        generic_subpart = Subpart(
            label=part.part_number,
            title="General",
            version=PAYLOAD.version
        )
        generic_subpart.save()
        PAYLOAD.subparts['section_subparts'].append(generic_subpart)
        parse_sections(part_soup.find_all('DIV8'), part, generic_subpart)
    else:
        for element in labeled_subparts:
            _subpart = Subpart(
                title=element.find('HEAD').text.strip(),
                label=part.part_number,
                version=PAYLOAD.version
            )
            _subpart.save()
            PAYLOAD.subparts['section_subparts'].append(_subpart)
            subpart_sections = element.find_all('DIV8')
            parse_sections(subpart_sections, part, _subpart)


def pre_process_tags(paragraph_element):
    """
    Convert initial italics-tagged text to markdown bold
    and convert the rest of a paragraph's I tags to markdown italics.
    """
    first_tag = paragraph_element.find('I')
    if first_tag:
        bold_content = first_tag.text
        first_tag.replaceWith('**{}**'.format(bold_content))
    for element in paragraph_element.find_all('I'):
        i_content = element.text
        element.replaceWith('*{}*'.format(i_content))
    return paragraph_element


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


def parse_appendix_graph(p_element):
    """Extract dot-based IDs, if any"""
    graph_text = ''
    id_match = re.match(dot_id_patterns['any'], p_element.text)
    if id_match:
        id_token = id_match.group(1)
        LEVEL_STATE.next_token = id_token
        pid = LEVEL_STATE.next_appendix_id()
        graph_text += "\n{" + pid + "}\n"
        graph = p_element.text.replace(
            '{}.'.format(pid), '**{}.**'.format(pid), 1).replace(
            '  ', ' ').replace(
            '** **', ' ', 1)
        graph_text += graph + "\n"
    else:
        graph_text += p_element.text + "\n"
    return graph_text


def parse_appendix_paragraphs(p_elements, id_type):
    for p_element in p_elements:
        p = pre_process_tags(p_element)
        if id_type == 'section':
            p_content = parse_ids(p.text) + "\n"
            p.replaceWith(p_content)
        else:
            p_content = parse_appendix_graph(p) + "\n"
            p.replaceWith(p_content)


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


def sniff_appendix_id_type(paragraphs):
    """
    Detect whether an appendix follows the section paragraph indentation
    scheme (a-1-i-A-1-i) or the appendix scheme (1-a)

    The sniffer should return 'section', 'appendix', or None.
    """
    for graph in paragraphs[:10]:
        if graph.text.startswith('(a)'):
            return 'section'
        if graph.text.startswith('1.'):
            return 'appendix'


def parse_appendix_elements(appendix_soup):
    """
    For appendices, we can't just parse paragraphs because
    appendices can have embedded sub-headlines. So we need to parse
    the section as a whole to keep the subheds in place.

    eCFR XML doesn't have any HD4s.
    """
    paragraphs = appendix_soup.find_all('P')
    id_type = sniff_appendix_id_type(paragraphs)
    for citation in appendix_soup.find_all('CITA'):
        citation.replaceWith('')
    for tag in HEADLINE_MAP:
        subheds = appendix_soup.find_all(tag)
        for subhed in subheds:
            hed_content = HEADLINE_MAP[tag].format(subhed.text.strip())
            subhed.replaceWith(hed_content)
    if id_type is None:
        for p in paragraphs:
            pre_process_tags(p)
            p.replaceWith(p.text + "\n")
    else:
        parse_appendix_paragraphs(paragraphs, id_type)
    return appendix_soup.text


def parse_appendices(appendices, part):
    """
    Parse the list of appendices (minus interps) and send them along.
    """
    if not appendices:
        return
    subpart = PAYLOAD.subparts['appendix_subpart']
    for i, _appendix in enumerate(appendices):
        default_appendix_letter = int_to_alpha(i + 1).upper()
        default_label = "{}-{}".format(
            part.part_number, default_appendix_letter)
        if _appendix['N']:
            default_label = "{}-{}".format(
                part.part_number,
                _appendix['N'].replace('Appendix ', ''),
            )
        head_element = _appendix.find('HEAD')
        _hed = head_element.text.strip()
        head_element.replaceWith('')
        if _hed.startswith('Appendix MS '):
            default_label = '{}-MS'.format(part.part_number)
        elif _hed.startswith('Appendix MS'):
            ms_number = re.match(r'Appendix MS[-]?(\d{1})', _hed).group(1)
            default_label = "{}-MS{}".format(part.part_number, ms_number)
        appendix = Section(
            subpart=subpart,
            label=default_label,
            title=_hed,
            contents=parse_appendix_elements(_appendix)
        )
        appendix.save()

    PAYLOAD.appendices.append(appendix)


def parse_interps(interp_div, part, subpart):
    """
    Break down interpretations into individual section interpretations,
    and them process them by subpart, creating a mapping of references
    to be inserted in the related sections.
    """
    interp_numeric_pattern = r'Section \d{4}\.(\d{1,2}) '
    interp_appendix_pattern = r'Appendix ([A-Z]{1,2}) -'
    preamble = ''
    for tag in interp_div.find('HEAD').findNextSiblings():
        if tag.name == 'P':
            preamble += pre_process_tags(tag).text + "\n"
        else:
            break
    for citation in interp_div.find_all('CITA'):
        citation.replaceWith('')
    if len(interp_div.find_all('HD1')) > 2:
        subheadings = interp_div.find_all('HD1')
    else:
        h1_elements = interp_div.find_all('HD1')
        subheadings = interp_div.find_all('HD2')
        if h1_elements:
            subheadings = [h1_elements.pop(0)] + subheadings
        if h1_elements:
            subheadings += h1_elements
    for i, heading in enumerate(reversed(subheadings)):
        _hed = heading.text.strip()
        if re.match(interp_numeric_pattern, _hed):
            section_number = re.match(interp_numeric_pattern, _hed).group(1)
        elif re.match(interp_appendix_pattern, _hed):
            section_number = re.match(interp_appendix_pattern, _hed).group(1)
        elif _hed == 'Introduction':
            section_number = '0'
        else:
            section_number = 'X'
        label = "{}-Interp-{}".format(part.part_number, section_number)
        if i == len(subheadings) - 1:
            content = preamble
        else:
            content = ''
        sub_elements = heading.findNextSiblings()
        for element in sub_elements:
            if element.name == 'P':
                content += pre_process_tags(element).text + "\n"
            elif element.name == 'HD3':
                content += "\n### {}\n".format(element.text.strip())
            elif element.name == 'HD2':
                if heading.name == 'HD2':
                    element.replaceWith('')
                    break
                content += "\n## {}\n".format(element.text.strip())
            elif element.name == 'HD1':
                element.replaceWith('')
                break
            else:
                content += "\n{}\n".format(element.text.strip())
            element.replaceWith('')
        interp = Section(
            subpart=subpart,
            label=label,
            title=_hed,
            contents=content
        )
        interp.save()
        PAYLOAD.interpretations.append(interp)


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
        raise ValueError('Provided Part number is not a CFPB regulation.')
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
        if not ecfr_request.ok:
            logger.info(
                "ECFR request failed with code {} and reason {}".format(
                    ecfr_request.status_code, ecfr_request.reason))
            return
        ecfr_request.encoding = 'utf-8'
        markup = ecfr_request.text
    soup = bS(markup, "lxml-xml")
    parts = soup.find_all('DIV5')
    part_soup = [div for div in parts if div['N'] == part_number][0]
    PAYLOAD.effective_date = get_effective_date(part_number)
    part = parse_part(part_soup, part_number)
    parse_version(part_soup, part)
    # parse_subparts will create and associate sections and appendices
    parse_subparts(part_soup, part)
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
            "[PART NUMBER or 'ALL'] [OPTIONAL XML FILE PATH]")
        sys.exit(1)
    elif len(args) == 1:
        if args[0] == 'ALL':
            for part in LEGACY_PARTS:
                logger.info("parsing {} from the latest eCFR XML".format(part))
                logger.info(ecfr_to_regdown(part))
        else:
            logger.info("parsing {} from the latest eCFR XML".format(args[0]))
            logger.info(ecfr_to_regdown(args[0]))
    else:
        if args[0] == 'ALL':
            for part in LEGACY_PARTS:
                logger.info('parsing {} from local XML file'.format(part))
                logger.info(ecfr_to_regdown(part, file_path=args[1]))
        else:
            logger.info('parsing {} from local XML file'.format(args[0]))
            logger.info(ecfr_to_regdown(args[0], file_path=args[1]))

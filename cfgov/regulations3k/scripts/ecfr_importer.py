import datetime
import logging
import re
import sys

import requests
from bs4 import BeautifulSoup as bS

from regulations3k.models.django import Section, Subpart
from regulations3k.parser.integer_conversion import int_to_alpha
from regulations3k.parser.paragraphs import (
    bold_first_italics,
    combine_bolds,
    graph_top,
    lint_paragraph,
    pre_process_tags,
)
from regulations3k.parser.patterns import (
    IdLevelState,
    dot_id_patterns,
    interp_inferred_section_pattern,
    interp_reference_pattern,
    paren_id_patterns,
)
from regulations3k.parser.payload import CFR_TITLE, PayLoad
from regulations3k.parser.regtable import RegTable


logger = logging.getLogger(__name__)

# eCFR globals
PART_ALLOWLIST = [
    "1001",
    "1002",
    "1003",
    "1004",
    "1005",
    "1006",
    "1007",
    "1008",
    "1009",
    "1010",
    "1011",
    "1012",
    "1013",
    "1014",
    "1015",
    "1016",
    "1022",
    "1024",
    "1025",
    "1026",
    "1030",
    "1041",
    "1070",
    "1071",
    "1072",
    "1073",
    "1074",
    "1075",
    "1076",
    "1080",
    "1081",
    "1082",
    "1083",
    "1090",
    "1091",
]
LEGACY_PARTS = [
    "1002",
    "1003",
    "1004",
    "1005",
    "1010",
    "1011",
    "1012",
    "1013",
    "1024",
    "1026",
    "1030",
]
INFERRED_SECTION_IDS = ["1030"]
# The latest eCFR version of title-12, updated every few days
LATEST_ECFR = (
    "https://www.gpo.gov/fdsys/bulkdata/ECFR/"
    "title-{0}/ECFR-title{0}.xml".format(CFR_TITLE)
)
HEADLINE_MAP = {
    "HD1": "\n## {}\n",
    "HD2": "\n### {}\n",
    "HD3": "\n#### {}\n",
}
LINK_FARM_TAGS = ["XREF", "FP-1", "FP-2"]
PAYLOAD = PayLoad()
LEVEL_STATE = IdLevelState()


def parse_subparts(part_soup, part):
    """
    Create subparts and the elements they contain.

    We need to parse appendices first so that, if there are interpretations,
    we have a mapping of interpretation references to insert into sections
    during section parsing.
    """
    subpart_list = part_soup.find_all("DIV6")
    appendix_subpart = Subpart(
        title="Appendices",
        label="Appendices",
        subpart_type=Subpart.APPENDIX,
        version=PAYLOAD.version,
    )
    appendix_subpart.save()
    PAYLOAD.subparts["appendix_subpart"] = appendix_subpart
    interp_subpart = Subpart(
        title="Supplement I to Part {} - Official Interpretations".format(
            part.part_number
        ),
        label="Interpretations",
        subpart_type=Subpart.INTERPRETATION,
        version=PAYLOAD.version,
    )
    appendices = part_soup.find_all("DIV9")
    if appendices:
        if appendices[-1].find("HEAD").text.startswith("Supplement I"):
            interp_subpart.save()
            PAYLOAD.subparts["interp_subpart"] = interp_subpart
            interp_div = appendices.pop(-1)
            parse_interps(interp_div, part, interp_subpart)
            LEVEL_STATE.current_id = ""
        parse_appendices(appendices, part)
        LEVEL_STATE.current_id = ""
    labeled_subparts = [subp for subp in subpart_list if subp.find("HEAD").text.strip()]
    if not labeled_subparts:
        generic_subpart = Subpart(
            label=part.part_number,
            subpart_type=Subpart.BODY,
            title="Sections",
            version=PAYLOAD.version,
        )
        generic_subpart.save()
        PAYLOAD.subparts["section_subparts"].append(generic_subpart)
        parse_sections(part_soup.find_all("DIV8"), part, generic_subpart)
    else:
        for element in labeled_subparts:
            _subpart = Subpart(
                title=element.find("HEAD").text.strip(),
                label=part.part_number,
                subpart_type=Subpart.BODY,
                version=PAYLOAD.version,
            )
            _subpart.save()
            PAYLOAD.subparts["section_subparts"].append(_subpart)
            subpart_sections = element.find_all("DIV8")
            parse_sections(subpart_sections, part, _subpart)


def parse_singleton_graph(graph_text, label):
    """Take a paragraph with a single ID and return styled with a braced ID"""
    new_graph = ""
    id_refs = PAYLOAD.interp_refs.get(label)
    id_match = re.search(paren_id_patterns["initial"], graph_top(graph_text))
    linted = lint_paragraph(combine_bolds(graph_text))
    if not id_match:
        return "\n" + linted + "\n"
    id_token = id_match.group(1).strip("*")
    if not LEVEL_STATE.token_validity_test(id_token):
        return "\n" + linted + "\n"
    LEVEL_STATE.next_token = id_token
    pid = LEVEL_STATE.next_id()
    if pid:
        new_graph += "\n{" + pid + "}\n"
    new_graph += linted + "\n"
    if id_refs and pid in id_refs:
        new_graph += "\n" + id_refs[pid] + "\n"
    return new_graph


def parse_multi_id_graph(graph, ids, label):
    """
    Parse a graph with 1 to 3 ids and return
    individual graphs with their own braced IDs.
    """
    new_graphs = ""
    id_refs = PAYLOAD.interp_refs.get(label)
    LEVEL_STATE.next_token = ids[0]
    pid1 = LEVEL_STATE.next_id()
    split1 = graph.partition("({})".format(ids[1]))
    text1 = lint_paragraph(combine_bolds(split1[0]))
    pid2_marker = split1[1]
    remainder = bold_first_italics(split1[2])
    new_graphs += "\n{" + pid1 + "}\n"
    new_graphs += text1 + "\n"
    if id_refs and pid1 in id_refs:
        new_graphs += "\n" + id_refs[pid1] + "\n"
    LEVEL_STATE.next_token = ids[1]
    pid2 = LEVEL_STATE.next_id()
    new_graphs += "\n{" + pid2 + "}\n"
    if len(ids) == 2:
        text2 = lint_paragraph(combine_bolds(" ".join([pid2_marker, remainder])))
        new_graphs += text2 + "\n"
        if id_refs and pid2 in id_refs:
            new_graphs += "\n" + id_refs[pid2] + "\n"
        return new_graphs
    else:
        split2 = remainder.partition("({})".format(ids[2]))
        pid3_marker = split2[1]
        remainder2 = bold_first_italics(split2[2])
        text2 = lint_paragraph(combine_bolds(" ".join([pid2_marker, split2[0]])))
        new_graphs += text2 + "\n"
        LEVEL_STATE.next_token = ids[2]
        pid3 = LEVEL_STATE.next_id()
        new_graphs += "\n{" + pid3 + "}\n"
        text3 = lint_paragraph(combine_bolds(" ".join([pid3_marker, remainder2])))
        new_graphs += text3 + "\n"
        if id_refs and pid3 in id_refs:
            new_graphs += "\n" + id_refs[pid3] + "\n"
        return new_graphs


def parse_ids(graph, label):
    """
    Extract up to three valid element IDs (indentaion markers)
    from a paragraph, and return a paragraph for each ID found.
    """
    raw_ids = re.findall(paren_id_patterns["initial"], graph_top(graph))
    clean_ids = [bit.strip("*") for bit in raw_ids if bit][:3]
    for clean_id in clean_ids:
        #  clean up edge-case bolding caused by italicized IDs, such as
        #  '(F)(<I>1</I>)' from reg 1026.7
        graph = graph.replace("**{}**".format(clean_id), clean_id)
    valid_ids = LEVEL_STATE.multiple_id_test(clean_ids)
    if not valid_ids or LEVEL_STATE.level() == 6:
        return parse_singleton_graph(graph, label)
    else:
        return parse_multi_id_graph(graph, valid_ids, label)


def parse_section_paragraphs(paragraph_soup, label):
    paragraph_content = ""
    for p in paragraph_soup:
        p = pre_process_tags(p)
        graph = p.text.replace("\n", "")
        paragraph_content += parse_ids(graph, label)
    return paragraph_content


def parse_interp_graph(p_element):
    """Extract dot-based IDs, if any."""
    graph_text = ""
    id_match = re.match(dot_id_patterns["any"], p_element.text)
    if id_match:
        id_token = id_match.group(1).replace("*", "")
        LEVEL_STATE.next_token = id_token
        pid = LEVEL_STATE.next_interp_id()
        graph_text += "\n{" + pid + "}\n"
        graph = (
            p_element.text.replace("{}.".format(pid), "**{}.**".format(pid), 1)
            .replace("  ", " ")
            .replace("** **", " ", 1)
            .replace("\n", "")
        )
        graph_text += graph + "\n"
    else:
        graph_text += p_element.text.replace("\n", "") + "\n"
    return graph_text


def parse_appendix_paragraphs(p_elements, id_type, label):
    for p_element in p_elements:
        p = pre_process_tags(p_element)
        if id_type == "section":
            p_content = parse_ids(p.text, label) + "\n"
            p.replaceWith(lint_paragraph(p_content))
        else:
            p_content = LEVEL_STATE.parse_appendix_graph(p, label) + "\n"
            p.replaceWith(lint_paragraph(p_content))


def parse_sections(section_list, part, subpart):
    for section_element in section_list:
        label = section_element["N"].rsplit(".")[-1]
        LEVEL_STATE.current_id = "a"
        section_content = parse_section_paragraphs(section_element.find_all("P"), label)
        _section = Section(
            subpart=subpart,
            label=label,
            title=section_element.find("HEAD").text.strip().replace("\xc2", ""),
            contents=section_content,
        )
        _section.save()


def set_table(table_soup, label):
    table = RegTable(label=label)
    msg = table.parse_xml_table(table_soup)
    if msg:
        PAYLOAD.tables.update({label: table})
    return msg


def parse_appendix_elements(appendix_soup, label):
    """
    For appendices, we can't just parse paragraphs because
    appendices can have embedded sub-headlines. So we need to parse
    the section as a whole to keep the subheds in place.

    eCFR XML doesn't have any HD4s.
    """
    paragraphs = appendix_soup.find_all("P")
    tables = appendix_soup.find_all("TABLE")
    for i, table_soup in enumerate(tables):
        table_label = "{{table-{}-{}}}".format(label, i)
        if set_table(table_soup, table_label):
            table_soup.replaceWith("\n{}\n".format(table_label))
    for form_line in appendix_soup.find_all("FP-DASH"):
        form_line.string = form_line.text.replace("\n", "") + "__\n"
    for i, image in enumerate(appendix_soup.find_all("img")):
        ref = "![image-{}-{}]({})".format(label, i + 1, image.get("src"))
        image.replaceWith("\n{}\n".format(ref))
    LEVEL_STATE.current_id = ""
    id_type = LEVEL_STATE.sniff_appendix_id_type(paragraphs)
    for citation in appendix_soup.find_all("CITA"):
        citation.replaceWith("")
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
        parse_appendix_paragraphs(paragraphs, id_type, label)
    result = appendix_soup.text
    for table_id in PAYLOAD.tables:
        result = result.replace(table_id, PAYLOAD.tables[table_id].table())
    return result


def get_appendix_label(n_value, head, default_label):
    """
    Avoid the pitfalls of non-standard appendix labels.

    Most DIV9 appendices have "N" values that reveal an appendix label.
    The default assures that we at least have a unique, sequential letter label
    so that the importer doesn't introduce runtime errors with a blank label.
    """

    def clean_label(label, term):
        return (
            label.replace(term, "")
            .replace(" and ", "")
            .replace("-", "")
            .replace(" ", "")
        )

    if n_value and " MS" not in n_value:
        return clean_label(n_value, "Appendix")
    if " to " in head or " - " in head:
        label_base = head.partition(" to ")[0].partition(" - ")[0]
        for term in ["Appendixes", "Appendix", "Appendices"]:
            if term in label_base:
                return clean_label(label_base, term)
    return default_label


def parse_appendices(appendices, part):
    """
    Process the list of appendices (minus interps) and send them along.
    """
    if not appendices:
        return
    subpart = PAYLOAD.subparts["appendix_subpart"]
    for i, _appendix in enumerate(appendices):
        n_value = _appendix["N"]
        head = _appendix.find("HEAD").text.strip()
        _appendix.find("HEAD").replaceWith("")
        default_label = int_to_alpha(i + 1).upper()
        label = get_appendix_label(n_value, head, default_label)
        if PAYLOAD.interp_refs and label in PAYLOAD.interp_refs:
            prefix = PAYLOAD.interp_refs[label]["1"] + "\n"
        else:
            prefix = ""
        appendix = Section(
            subpart=subpart,
            label=label,
            title=head,
            contents=prefix + parse_appendix_elements(_appendix, default_label),
        )
        appendix.save()

    PAYLOAD.appendices.append(appendix)


def divine_interp_tag_use(element, part_num):
    """
    Try to determine what an interpretation element is delivering.

    Interp elements wear many hats.
    HD elements might be announcing an intro, a subpart, a section,
    an appendix or appendices, or a paragraph reference.

    - HD1 elements might denote intros, sections, or subparts
    - HD2 elements might denote sections or paragraph references
    - HD3 elements might denote sections or paragraph references

    P elements might be paragraph references or plain interp paragraphs.

    The function will return one of these values:
    - intro
    - subpart
    - section
    - appendix
    - appendices
    - graph_id
    - graph_id_inferred_section -- a treat found in Reg DD
    - '' (Denoting no use found -- render as an interp paragraph)
    """
    text = element.text.strip()
    if "INTRODUCTION" in text.upper():
        return "intro"
    if text.startswith("Section") or text.startswith("\N{SECTION SIGN}"):
        return "section"
    if text.startswith("Appendix"):
        return "appendix"
    if text.startswith("Appendices") or text.startswith("Appendixes"):
        return "appendices"
    if re.match(r"\d{1,3}\([a-z]{1,2}\)", text.replace("Paragraph", "", 1).strip()):
        return "graph_id"
    if (
        re.match(r"\([a-z]{1,2}\)", text.replace("Paragraph", "", 1).strip())
        and part_num in INFERRED_SECTION_IDS
    ):
        return "graph_id_inferred_section"
    return ""


def parse_interp_graph_reference(element, part_num, section_tag):
    """Extract and return a graph reference from an element."""
    id_text = element.text.replace("Paragraph", "", 1).strip()
    id_match = re.match(interp_reference_pattern, id_text)
    if id_match:
        tokens = [token.strip("()") for token in id_match.groups() if token]
        tokens.append("Interp")
        return "-".join(tokens)
    elif (
        re.match(interp_inferred_section_pattern, id_text)
        and part_num in INFERRED_SECTION_IDS
    ):
        id_match = re.match(interp_inferred_section_pattern, id_text)
        tokens = (
            [section_tag]
            + [token.strip("()") for token in id_match.groups() if token]
            + ["Interp"]
        )
        return "-".join(tokens)
    else:
        return ""


def get_interp_section_tag(headline):
    """ "Derive an interp section tag from the HD content."""

    interp_numeric_pattern = r"(?:Section|\xa7) \d{4}\.(\d{1,3}) "
    if headline.upper() == "INTRODUCTION":
        return "0"
    if re.match(interp_numeric_pattern, headline):
        return re.match(interp_numeric_pattern, headline).group(1)
    else:
        return get_appendix_label("", headline, headline.partition(" ")[0])


def register_interp_reference(interp_id, section_tag):
    """
    Registers an interp reference mapping that can be used, when parsing
    section paragraphs, to insert a regdown interp reference.

    This also resets LEVEL_STATE.current_id for parsing the current section.
    """

    section_label = section_tag
    graph_id = "-".join(interp_id.split("-")[1:-1])
    LEVEL_STATE.current_id = interp_id
    if section_label not in PAYLOAD.interp_refs:
        PAYLOAD.interp_refs[section_label] = {}
    PAYLOAD.interp_refs[section_label].update(
        {graph_id: "see({}-{}-Interp)".format(section_tag, graph_id)}
    )


def parse_interps(interp_div, part, subpart):
    """
    Break up interpretations by reg section, and then create a mapping
    of interp references to be inserted in the related regdown.

    Example: Reg B section 1002.2, paragraph {c-1-ii}

    If that paragraph had an interpretation, the interp reference would be:

    see(2-c-1-ii-Interp)

    This would refer to a part of interpretation section 1002-Interp-2

    In that file, the related content would need to be marked with this ID:

    {2-c-1-ii-Interp}

    Any interp subgraphs would get picked up too. Subgraph 1 would get this ID:

    {2-c-1-ii-Interp-1}
    """

    section_headings = [
        tag
        for tag in interp_div.find("HEAD").findNextSiblings()
        if (
            tag.name in ["HD1", "HD2", "HD3"]
            and divine_interp_tag_use(tag, part.part_number)
            in ["intro", "section", "appendix", "appendices"]
        )
    ]
    for section_heading in section_headings:
        LEVEL_STATE.current_id = ""
        section_hed = section_heading.text.strip()
        section_label = get_interp_section_tag(section_hed)
        interp_section_label = "Interp-{}".format(section_label)
        section = Section(
            subpart=subpart,
            label=interp_section_label,
            title=section_hed.replace("Section ", "Comment for ")
            .replace("\xa7", "Comment for ")
            .replace("Appendix ", "Comment for Appendix "),
            contents="",
        )
        if divine_interp_tag_use(section_heading, part.part_number) == "appendix":
            interp_id = "{}-1-Interp".format(section_label)
            LEVEL_STATE.current_id = interp_id
            see = "see({}-1-Interp)".format(section_label)
            ref = {section_label: {"1": see}}
            PAYLOAD.interp_refs.update(ref)
        for element in section_heading.findNextSiblings():
            if element in section_headings:
                section.save()
                PAYLOAD.interpretations.append(section)
                break
            if element.name in ["HD1", "XREF", "CITA"]:
                continue
            if element.name in ["HD2", "HD3"] and divine_interp_tag_use(
                element, part.part_number
            ) in ["graph_id", "graph_id_inferred_section"]:
                _hed = element.text.strip()
                interp_id = parse_interp_graph_reference(
                    element, part.part_number, section_label
                )
                register_interp_reference(interp_id, section_label)
                section.contents += "\n{" + interp_id + "}\n"
                section.contents += "### {}\n".format(_hed)
            elif element.name == "P":
                tag_use = divine_interp_tag_use(element, part.part_number)
                if tag_use in ["graph_id", "graph_id_inferred_section"]:
                    interp_id = parse_interp_graph_reference(
                        element, part.part_number, section_label
                    )
                    register_interp_reference(interp_id, section_label)
                    section.contents += "\n{" + interp_id + "}\n"
                    if tag_use == "graph_id_inferred_section":
                        element.insert(0, section_label)
                    section.contents += "### {}\n".format(element.text.strip())
                else:
                    p = pre_process_tags(element)
                    section.contents += parse_interp_graph(p)
            else:
                section.contents += "\n{}\n".format(element.text.strip())
        section.save()
        if section not in PAYLOAD.interpretations:
            PAYLOAD.interpretations.append(section)


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

    To avoid mischief, we make sure the part number is on an allowlist.
    """
    PAYLOAD.reset()
    if part_number not in PART_ALLOWLIST:
        raise ValueError("Provided Part number is not a CFPB regulation.")
    starter = datetime.datetime.now()
    if file_path:
        try:
            with open(file_path, "r") as f:
                markup = f.read()
        except IOError:
            logger.info("Could not open local file {}".format(file_path))
            return
    else:
        ecfr_request = requests.get(LATEST_ECFR)
        if not ecfr_request.ok:
            logger.info(
                "ECFR request failed with code {} and reason {}".format(
                    ecfr_request.status_code, ecfr_request.reason
                )
            )
            return
        ecfr_request.encoding = "utf-8"
        markup = ecfr_request.text
    soup = bS(markup, "lxml-xml")
    parts = soup.find_all("DIV5")
    part_soup = [div for div in parts if div["N"] == part_number][0]
    PAYLOAD.get_effective_date(part_number)
    PAYLOAD.parse_part(part_soup, part_number)
    part = PAYLOAD.part
    PAYLOAD.parse_version(part_soup, part)
    # parse_subparts will create and associate sections and appendices
    parse_subparts(part_soup, part)
    msg = "Draft version of Part {} created.\n" "Parsing took {}".format(
        part_number, (datetime.datetime.now() - starter)
    )
    return msg


def run(*args):
    if len(args) not in [1, 2]:
        logger.info(
            "Usage: ./cfgov/manage.py runscript "
            "ecfr_importer --script-args "
            "[PART NUMBER or 'ALL'] [OPTIONAL XML FILE PATH]"
        )
        sys.exit(1)
    elif len(args) == 1:
        if args[0] == "ALL":
            starter = datetime.datetime.now()
            for part in LEGACY_PARTS:
                logger.info("parsing {} from the latest eCFR XML".format(part))
                logger.info(ecfr_to_regdown(part))
            logger.info(
                "Overall, parsing took {}".format(datetime.datetime.now() - starter)
            )
        else:
            logger.info("parsing {} from the latest eCFR XML".format(args[0]))
            logger.info(ecfr_to_regdown(args[0]))
    else:
        if args[0] == "ALL":
            starter = datetime.datetime.now()
            for part in LEGACY_PARTS:
                logger.info("parsing {} from local XML file".format(part))
                logger.info(ecfr_to_regdown(part, file_path=args[1]))
            logger.info(
                "Overall, parsing took {}".format(datetime.datetime.now() - starter)
            )
        else:
            logger.info("parsing {} from local XML file".format(args[0]))
            logger.info(ecfr_to_regdown(args[0], file_path=args[1]))

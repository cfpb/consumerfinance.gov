"""
Provide string-manipulation functions for regulation paragraphs.

Paragraph parsing operations that manipulate paragraph IDs are handled
by the patterns.IdLevelState class.
"""

import re


def bold_first_italics(graph_text):
    """For a newly broken-up graph, convert the first italics text to bold."""
    if graph_text.count("*") > 1:
        return graph_text.replace("*", "**", 2)
    else:
        return graph_text


def combine_bolds(graph_text):
    """
    Make ID marker bold and remove redundant bold markup between bold elements.
    """
    if graph_text.startswith("("):
        graph_text = (
            graph_text.replace("  ", " ")
            .replace("(", "**(", 1)
            .replace(")", ")**", 1)
            .replace("** **", " ", 1)
        )
    return graph_text


def graph_top(graph_text):
    "Weed out the common sources of errant IDs"
    return (
        graph_text.partition("paragraph")[0]
        .partition("12 CFR")[0]
        .partition("\xa7")[0][:200]
    )


def lint_paragraph(graph_text):
    """Clean formatting anomalies.

    - Missing em dashes
    - restoring italics
    """
    fix1 = restore_emdash(graph_text)
    fix2 = restore_italics(fix1)
    return fix2


def restore_italics(graph_text):
    fix1 = re.sub(
        r"\*\*(see)\*\*", r"*\g<1>*", graph_text, flags=re.IGNORECASE
    )
    fix2 = re.sub(
        r"\*\*(et\.? seq\.? ?)\*\*?", r"*\g<1>*", fix1, flags=re.IGNORECASE
    )
    return fix2


def restore_emdash(graph_text):
    stripped = graph_text.rstrip()
    if stripped.endswith("-"):
        return stripped + "--\n"
    return graph_text


def pre_process_tags(paragraph_element):
    """
    Convert initial italics-tagged text to markdown bold
    and convert the rest of a paragraph's I tags to markdown italics.
    """
    first_tag = paragraph_element.find("I")
    if first_tag:
        bold_content = first_tag.text
        first_tag.replaceWith("**{}**".format(bold_content))
    for element in paragraph_element.find_all("I"):
        i_content = element.text
        element.replaceWith("*{}*".format(i_content))
    return paragraph_element

"""
Provide string-manipulation functions for regulation paragraphs.

Paragraph parsing operations that manipulate paragraph IDs are handled
by the patterns.IdLevelState class.
"""
from __future__ import unicode_literals


def bold_first_italics(graph_text):
    """For a newly broken-up graph, convert the first italics text to bold."""
    if graph_text.count('*') > 1:
        return graph_text.replace('*', '**', 2)
    else:
        return graph_text


def combine_bolds(graph_text):
    """
    Make ID marker bold and remove redundant bold markup between bold elements.
    """
    if graph_text.startswith('('):
        graph_text = graph_text.replace(
            '  ', ' ').replace(
            '(', '**(', 1).replace(
            ')', ')**', 1).replace(
            '** **', ' ', 1)
    return graph_text


def graph_top(graph_text):
    "Weed out the common sources of errant IDs"
    return graph_text.partition(
        'paragraph')[0].partition(
        '12 CFR')[0].partition(
        '\xa7')[0][:200]


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

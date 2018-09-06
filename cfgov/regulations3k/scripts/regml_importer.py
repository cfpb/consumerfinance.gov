from __future__ import unicode_literals

import datetime
import logging
import sys

from lxml import etree

from regulations3k.models.django import (
    EffectiveVersion, Part, Section, Subpart
)


logger = logging.getLogger(__name__)

CFR_CHAPTER = 'X'

TABLE_XSLT = b'''<?xml version='1.0' encoding='UTF-8'?>
<xsl:stylesheet version="1.0"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:eregs="eregs"
        exclude-result-prefixes="eregs">
    <xsl:output method="xml" omit-xml-declaration="yes" />
    <xsl:output encoding="UTF-8"/>

    <xsl:template match="eregs:table">
        <div class="o-table o-table-wrapper__scrolling">
            <table>
                <xsl:apply-templates select="eregs:header"/>
                <tbody>
                    <xsl:apply-templates select="eregs:row"/>
                </tbody>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="eregs:header">
        <thead>
            <xsl:apply-templates/>
        </thead>
    </xsl:template>

    <xsl:template match="eregs:columnHeaderRow">
        <tr>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>

    <xsl:template match="eregs:column">
        <th scope="col">
            <xsl:attribute name="rowspan">
                <xsl:value-of select="@rowspan"/>
            </xsl:attribute>
            <xsl:attribute name="colspan">
                <xsl:value-of select="@colspan"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </th>
    </xsl:template>

    <xsl:template match="eregs:row">
        <tr>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>

    <xsl:template match="eregs:cell">
        <td align="left">
            <xsl:apply-templates/>
        </td>
    </xsl:template>

</xsl:stylesheet>
'''
TABLE_TRANSFORM = etree.XSLT(etree.fromstring(TABLE_XSLT))


class RegMLParser(object):

    def parse(self, xml_tree, part=None, effective_version=None):
        # Strip tags we're not interested in
        etree.strip_tags(xml_tree, '{eregs}ref')
        etree.strip_tags(xml_tree, '{eregs}def')
        etree.strip_tags(xml_tree, '{eregs}callout')
        etree.strip_tags(xml_tree, '{eregs}line')
        etree.strip_tags(xml_tree, '{eregs}variable')
        etree.strip_tags(xml_tree, '{eregs}subscript')

        if part is None:
            part = self.get_part(xml_tree)

        if effective_version is None:
            effective_version = self.get_effective_version(part, xml_tree)

        subpart_nodes = xml_tree.findall(
            './{eregs}part/{eregs}content/{eregs}subpart'
        )
        appendix_nodes = xml_tree.findall(
            './{eregs}part/{eregs}content/{eregs}appendix'
        )
        interp_node = xml_tree.find(
            './{eregs}part/{eregs}content/{eregs}interpretations'
        )

        if subpart_nodes is not None:
            self.get_subparts(
                effective_version, subpart_nodes, interp_node=interp_node
            )

        if appendix_nodes is not None:
            self.get_appendices(
                effective_version, appendix_nodes, interp_node=interp_node
            )

        if interp_node is not None:
            self.get_interpretations(effective_version, interp_node)

        return effective_version

    def get_part(self, xml_tree):
        part_number = xml_tree.find(
            './{eregs}preamble/{eregs}cfr/{eregs}section'
        ).text
        cfr_title = xml_tree.find(
            './{eregs}preamble/{eregs}cfr/{eregs}title'
        ).text
        part, created = Part.objects.get_or_create(
            part_number=part_number,
            chapter=CFR_CHAPTER,
            cfr_title_number=cfr_title)

        return part

    def get_effective_version(self, part, xml_tree):
        effective_date_str = xml_tree.find(
            './{eregs}preamble/{eregs}effectiveDate'
        ).text
        effective_date = datetime.datetime.strptime(
            effective_date_str, "%Y-%m-%d"
        ).date()
        effective_version, created = \
            EffectiveVersion.objects.get_or_create(
                effective_date=effective_date,
                part=part
            )

        if not created:
            raise ValueError(
                'Effecitve date {} already exists for part {}'.format(
                    effective_date, part)
            )

        effective_version.draft = True
        return effective_version

    def get_subparts(self, effective_version, subpart_nodes,
                     interp_node=None):
        subparts = []
        for subpart_node in subpart_nodes:
            label = subpart_node.get('label')
            letter = subpart_node.get('subpartLetter')

            title_text = ''
            title_node = subpart_node.find('{eregs}title')
            if title_node is not None:
                title_text = title_node.text

            title = 'Subpart {letter} - {title_text}'.format(
                letter=letter,
                title_text=title_text
            )

            subpart_type = Subpart.BODY
            subpart = Subpart(
                label=label,
                title=title,
                version=effective_version,
                subpart_type=subpart_type
            )
            subpart.save()

            logger.info('Created subpart {}'.format(subpart))

            section_nodes = subpart_node.findall(
                './{eregs}content/{eregs}section'
            )
            for section_node in section_nodes:
                self.get_section_for_node(
                    subpart, section_node, interp_node=interp_node
                )

            subparts.append(subpart)

        return subparts

    def get_appendices(self, effective_version, appendix_nodes,
                       interp_node=None):
        subpart_type = Subpart.APPENDIX
        subpart = Subpart(
            label='Appendices',
            title='Appendices',
            version=effective_version,
            subpart_type=subpart_type
        )
        subpart.save()
        logger.info('Created appendix subpart {}'.format(subpart))

        for appendix_node in appendix_nodes:
            self.get_section_for_appendix(
                subpart, appendix_node, interp_node=interp_node
            )

        return subpart

    def get_interpretations(self, effective_version, interp_node):
        regml_label = interp_node.get('label')
        label = regml_label.split('-', 1)[1]
        title = interp_node.find('./{eregs}title').text
        subpart_type = Subpart.INTERPRETATION
        subpart = Subpart(
            label=label,
            title=title,
            version=effective_version,
            subpart_type=subpart_type
        )
        subpart.save()
        logger.info('Created interpretations subpart {}'.format(subpart))

        section_nodes = interp_node.findall(
            './{eregs}interpSection'
        )
        for section_node in section_nodes:
            self.get_section_for_interp_section_node(
                subpart, section_node
            )

        return subpart

    def get_section_for_node(self, subpart, section_node, interp_node=None):
        regml_label = section_node.get('label')
        label = regml_label.split('-', 1)[1]
        title = section_node.find('./{eregs}subject').text
        contents = ''

        paragraph_nodes = section_node.findall(
            './{eregs}paragraph'
        )
        for paragraph_node in paragraph_nodes:
            contents += self.get_regdown_for_paragraph(
                paragraph_node, interp_node=interp_node
            )

        section = Section(
            label=label,
            title=title,
            contents=contents,
            subpart=subpart
        )
        section.save()
        logger.info('Created section {}'.format(title))
        return section

    def get_section_for_appendix(self, subpart, appendix_node,
                                 interp_node=None):
        regml_label = appendix_node.get('label')
        label = regml_label.split('-', 1)[1]
        title = appendix_node.find('{eregs}appendixTitle').text
        contents = ''

        section_nodes = appendix_node.findall('{eregs}appendixSection')
        for section_node in section_nodes:
            section_regml_label = appendix_node.get('label')
            section_label = section_regml_label.split('-', 1)[1]
            contents += '{{{label}}}\n'.format(label=section_label)

            section_subject = section_node.find('{eregs}subject').text
            contents += '## {subject}\n\n'.format(subject=section_subject)

            paragraph_nodes = section_node.findall(
                './{eregs}paragraph'
            )
            for paragraph_node in paragraph_nodes:
                contents += self.get_regdown_for_paragraph(
                    paragraph_node, interp_node=interp_node
                )

        section = Section(
            label=label,
            title=title,
            contents=contents,
            subpart=subpart
        )
        section.save()
        logger.info('Created appendix {}'.format(title))

        return section

    def get_section_for_interp_section_node(self, subpart, section_node):
        regml_label = section_node.get('label').replace('_', '')
        label = regml_label.split('-', 1)[1]
        # With Regs3k we've flipped interpretation section labels.
        label = '{1}-{0}'.format(*label.split('-', 2))

        title = section_node.find('./{eregs}title').text
        contents = ''

        paragraph_nodes = section_node.findall(
            './{eregs}interpParagraph'
        )
        for paragraph_node in paragraph_nodes:
            contents += self.get_regdown_for_paragraph(paragraph_node)

        section = Section(
            label=label,
            title=title,
            contents=contents,
            subpart=subpart
        )
        section.save()
        logger.info('Created interpretation section {}'.format(label))
        return section

    def get_regdown_for_paragraph(self, paragraph_node, interp_node=None):
        regdown = ''

        regml_label = paragraph_node.get('label')
        if regml_label is not None:
            label = regml_label.split('-', 2)[2]
            regdown += '{{{label}}}\n'.format(label=label)

        marker = paragraph_node.get('marker')

        title = ''
        title_node = paragraph_node.find('{eregs}title')
        if title_node is not None and title_node.text is not None:
            title = ' ' + title_node.text

        if marker or title:
            regdown += '**{marker}{title}** '.format(
                marker=marker, title=title
            )

        content_node = paragraph_node.find('{eregs}content')
        contents = content_node.text or ''
        for child_node in content_node:
            if child_node.tag == '{eregs}dash':
                contents += '{text}__{tail}'.format(
                    text=child_node.text or ' ', tail=child_node.tail or ''
                )
            elif child_node.tag == '{eregs}graphic':
                alttext = child_node.find('./{eregs}altText').text or ''
                url = child_node.find('./{eregs}url').text or ''
                contents += '![{alttext}]({url})'.format(
                    alttext=alttext, url=url
                )
            elif child_node.tag == '{eregs}table':
                table_string = etree.tostring(
                    TABLE_TRANSFORM(child_node)
                ).decode()
                contents += table_string.replace('\n', '').replace('\r', '')

        regdown += '{contents}\n\n'.format(
            contents=contents
        )

        if interp_node is not None and regml_label is not None:
            interp_nodes_targetting_paragraph = [
                n for n in interp_node.findall(
                    './/{eregs}interpParagraph[@target]'
                )
                if n.get('target') == regml_label
            ]
            for interp_node in interp_nodes_targetting_paragraph:
                interp_regml_label = interp_node.get('label')
                interp_label = interp_regml_label.split('-', 1)[1]
                regdown += '\nsee({interp_label})\n\n'.format(
                    interp_label=interp_label
                )

        # Get all subparagraphs of this paragraph type
        subparagraph_nodes = paragraph_node.findall(paragraph_node.tag)
        for subparagraph_node in subparagraph_nodes:
            regdown += self.get_regdown_for_paragraph(subparagraph_node)

        return regdown


def regml_to_regdown(regulation_file):
    '''
    Extract an effective version of a regulation from RegML and create regdown
    content.
    '''
    starter = datetime.datetime.now()

    try:
        with open(regulation_file, 'rb') as f:
            reg_xml = f.read()
    except IOError:
        logger.info('Could not open local file {}'.format(regulation_file))
        return

    parser = etree.XMLParser(huge_tree=True, remove_blank_text=True)
    xml_tree = etree.fromstring(reg_xml, parser)
    parser = RegMLParser()
    effective_version = parser.parse(xml_tree)

    msg = (
        'Draft {version} version of part {part} created.\n'
        'Parsing took {time}'.format(
            version=effective_version,
            part=effective_version.part.part_number,
            time=(datetime.datetime.now() - starter)
        )
    )
    return msg


def run(*args):
    if len(args) != 1:
        logger.info(
            'Usage: ./cfgov/manage.py runscript '
            'regml_importer --script-args '
            '[REGML FILE PATH]')
        sys.exit(1)
    else:
        logger.info('Parsing from RegML file {}'.format(args[0]))
        logger.info(regml_to_regdown(args[0]))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.conf import settings
from django.test import TestCase

import mock
from lxml import etree
from model_mommy import mommy

from regulations3k.models.django import EffectiveVersion, Part, Subpart
from regulations3k.scripts import regml_importer


class RegMLImporterTestCase(TestCase):

    def setUp(self):
        self.part = mommy.make(
            Part,
            chapter='X',
            cfr_title_number='12',
            part_number='1005',
        )
        self.effective_version = mommy.make(
            EffectiveVersion,
            effective_date=date(2018, 1, 1),
            part=self.part,
            draft=True
        )
        self.subpart = mommy.make(Subpart)

        self.parser = regml_importer.RegMLParser()

        self.regml_file = "{}/regulations3k/fixtures/reg_d.regml".format(
            settings.PROJECT_ROOT
        )

    @mock.patch('logging.Logger.info')
    def test_script_run(self, mock_info):
        regml_importer.run(self.regml_file)
        mock_info.assert_any_call(
            'Parsing from RegML file {}'.format(self.regml_file)
        )

    def test_script_run_without_argument(self):
        with self.assertRaises(SystemExit):
            regml_importer.run()

    def test_regml_to_regdown(self):
        msg = regml_importer.regml_to_regdown(self.regml_file)
        self.assertIn('version of part 1004 created', msg)

    @mock.patch('logging.Logger.info')
    def test_regml_to_regdown_file_does_not_exist(self, mock_info):
        regml_importer.regml_to_regdown('/some/non/existent/file')
        mock_info.assert_any_call(
            'Could not open local file /some/non/existent/file'
        )

    def test_parser_parse(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <regulation xmlns="eregs">
                <preamble>
                    <cfr>
                        <title>12</title>
                        <section>1005</section>
                    </cfr>
                    <effectiveDate>2016-11-14</effectiveDate>
                </preamble>
                <part label="1005">
                    <content>
                        <subpart subpartLetter="A" label="1005-Subpart-A">
                            <title>General</title>
                        </subpart>
                        <appendix appendixLetter="A" label="1005-A">
                            <appendixTitle>Appendix A</appendixTitle>
                        </appendix>
                        <interpretations label="1005-Interp">
                            <title>Supplement I to Part 1005</title>
                        </interpretations>
                    </content>
                </part>
            </regulation>'''
        xml_tree = etree.fromstring(regml)
        effective_version = self.parser.parse(xml_tree)
        self.assertEqual(effective_version.subparts.count(), 3)

    def test_regml_part(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <regulation xmlns="eregs">
                <preamble>
                    <cfr>
                        <title>12</title>
                        <section>1005</section>
                    </cfr>
                </preamble>
            </regulation>'''
        xml_tree = etree.fromstring(regml)
        part = self.parser.get_part(xml_tree)
        self.assertEqual(part, self.part)

    def test_regml_effective_version(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <regulation xmlns="eregs">
                <preamble>
                    <effectiveDate>2016-11-14</effectiveDate>
                </preamble>
            </regulation>'''
        xml_tree = etree.fromstring(regml)
        effective_version = self.parser.get_effective_version(
            self.part, xml_tree
        )
        self.assertEqual(
            effective_version.effective_date,
            date(2016, 11, 14)
        )

    def test_regml_effective_version_existing(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <regulation xmlns="eregs">
                <preamble>
                    <effectiveDate>2018-01-01</effectiveDate>
                </preamble>
            </regulation>'''
        xml_tree = etree.fromstring(regml)
        with self.assertRaises(ValueError):
            self.parser.get_effective_version(
                self.part, xml_tree
            )

    def test_regml_subpart(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <content xmlns="eregs">
                <subpart subpartLetter="A" label="1005-Subpart-A">
                    <title>General</title>
                    <content>
                        <section label="1005-1" sectionNum="1">
                            <subject>1005.1 Authority and purpose.</subject>
                        </section>
                    </content>
                </subpart>
                <subpart subpartLetter="B" label="1005-Subpart-B">
                    <title>Requirements for Remittance Transfers</title>
                </subpart>
            </content>'''
        subpart_nodes = etree.fromstring(regml).findall('{eregs}subpart')
        subparts = self.parser.get_subparts(
            self.effective_version, subpart_nodes
        )
        self.assertEqual(len(subparts), 2)
        self.assertEqual(subparts[0].title, 'Subpart A - General')
        self.assertEqual(subparts[0].sections.count(), 1)

    def test_regml_section(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <section xmlns="eregs" label="1005-1" sectionNum="1">
                <subject>1005.1 Authority and purpose.</subject>
                <paragraph xmlns="eregs" label="1005-1-a" marker="">
                    <content>
                        Test paragraph
                    </content>
                </paragraph>
            </section>'''
        section_node = etree.fromstring(regml)
        section = self.parser.get_section_for_node(
            self.subpart, section_node
        )
        self.assertEqual(section.label, '1')
        self.assertEqual(section.title, '1005.1 Authority and purpose.')
        self.assertIn('Test paragraph', section.contents)

    def test_regdown_appendices(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <regulation xmlns="eregs">
                <appendix appendixLetter="A" label="1005-A">
                    <appendixTitle>Appendix A</appendixTitle>
                </appendix>
            </regulation>'''
        appendix_nodes = etree.fromstring(regml).findall('{eregs}appendix')
        appendix_subpart = self.parser.get_appendices(
            self.effective_version, appendix_nodes
        )
        self.assertEqual(appendix_subpart.sections.count(), 1)

    def test_regdown_appendix_section(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <appendix xmlns="eregs" appendixLetter="A" label="1005-A">
                <appendixTitle>Appendix A</appendixTitle>
                <appendixSection appendixSecNum="1" label="1005-A-h1">
                    <subject>Section Subject</subject>
                    <paragraph label="1005-A-h1-p1" marker="">
                        <content>This is a paragraph.</content>
                    </paragraph>
                </appendixSection>
            </appendix>'''
        appendix_node = etree.fromstring(regml)
        appendix_section = self.parser.get_section_for_appendix(
            self.subpart, appendix_node
        )
        self.assertIn('## Section Subject', appendix_section.contents)

    def test_regdown_interpretations(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <interpretations xmlns="eregs" label="1005-Interp">
                <title>Supplement I to Part 1005</title>
                <interpSection label="1005-Interp-1">
                    <title>Introduction</title>
                </interpSection>
            </interpretations>'''
        interp_node = etree.fromstring(regml)
        interp_subpart = self.parser.get_interpretations(
            self.effective_version, interp_node
        )
        self.assertEqual(interp_subpart.title, 'Supplement I to Part 1005')
        self.assertEqual(interp_subpart.label, 'Interp')
        self.assertEqual(interp_subpart.sections.count(), 1)

    def test_regdown_interp_section(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <interpSection xmlns="eregs" label="1005-Interp-1">
                <title>Introduction</title>
                <interpParagraph label="1005-h1-Interp-1" marker="1.">
                    <title>General.</title>
                    <content>Commentary paragraph content.</content>
                </interpParagraph>
            </interpSection>'''
        interp_section_node = etree.fromstring(regml)
        interp_section = self.parser.get_section_for_interp_section_node(
            self.subpart, interp_section_node
        )
        self.assertEqual(interp_section.title, 'Introduction')
        self.assertEqual(interp_section.label, '1-Interp')
        self.assertIn('**1. General.**', interp_section.contents)
        self.assertIn('Commentary paragraph content', interp_section.contents)

    def test_regdown_paragraph_with_keyterm(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <paragraph xmlns="eregs" label="1005-1-a" marker="(a)">
                <title type="keyterm">Authority.</title>
                <content>
                    The regulation in this part, known as Regulation E,
                    is issued by the Bureau of Consumer Financial Protection
                </content>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)
        regdown = self.parser.get_regdown_for_paragraph(paragraph_node)
        self.assertIn('{a}', regdown)
        self.assertIn('**(a) Authority.**', regdown)

    def test_regdown_paragraph_without_keyterm(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <paragraph xmlns="eregs" label="1005-1-a" marker="(a)">
                <content>
                    The regulation in this part, known as Regulation E,
                    is issued by the Bureau of Consumer Financial Protection
                </content>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)
        regdown = self.parser.get_regdown_for_paragraph(paragraph_node)
        self.assertIn('{a}', regdown)
        self.assertIn('**(a)**', regdown)

    def test_regdown_paragraph_without_marker_or_keyterm(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <paragraph xmlns="eregs" label="1005-1-a" marker="">
                <content>
                    Test paragraph
                </content>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)
        regdown = self.parser.get_regdown_for_paragraph(paragraph_node)
        self.assertNotIn('****', regdown)

    def test_regdown_paragraph_with_subparagraph(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <paragraph xmlns="eregs" label="1005-1-a" marker="(a)">
                <content>
                    This is a paragraph.
                </content>
                <paragraph label="1005-1-a-1" marker="(1)">
                    <content>
                        This is a subparagraph.
                    </content>
                </paragraph>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)
        regdown = self.parser.get_regdown_for_paragraph(paragraph_node)
        self.assertIn('{a}', regdown)
        self.assertIn('**(a)**', regdown)
        self.assertIn('{a-1}', regdown)
        self.assertIn('**(1)**', regdown)
        self.assertIn('This is a paragraph', regdown)
        self.assertIn('This is a subparagraph', regdown)

    def test_regdown_paragraph_with_interp(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <paragraph xmlns="eregs" label="1005-1-a" marker="(a)">
                <content>
                    The regulation in this part, known as Regulation E,
                    is issued by the Bureau of Consumer Financial Protection
                </content>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)

        interp_regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <interpretations xmlns="eregs">
                <interpSection>
                    <interpParagraph label="1005-1-a-Interp" target="1005-1-a">
                    </interpParagraph>
                </interpSection>
            </interpretations>
        '''
        interp_node = etree.fromstring(interp_regml)

        regdown = self.parser.get_regdown_for_paragraph(
            paragraph_node, interp_node=interp_node
        )
        self.assertIn('see(1-a-Interp)', regdown)

    def test_regdown_paragraph_with_dash_field(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <paragraph xmlns="eregs" label="1005-1-a" marker="(a)">
                <content>
                    <dash>Name:</dash>
                </content>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)
        regdown = self.parser.get_regdown_for_paragraph(paragraph_node)
        self.assertIn('Name:__', regdown)

    def test_regdown_paragraph_with_dash_no_field(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <paragraph xmlns="eregs" label="1005-1-a" marker="(a)">
                <content>
                    <dash/>
                </content>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)
        regdown = self.parser.get_regdown_for_paragraph(paragraph_node)
        self.assertIn('__', regdown)

    def test_regdown_paragraph_with_graphic(self):
        regml = b'''<?xml version='1.0' encoding='UTF-8'?>
            <paragraph xmlns="eregs" label="1005-1-a" marker="(a)">
                <content>
                    <graphic>
                        <altText>image alt</altText>
                        <url>https:///images/image_name.png</url>
                    </graphic>
                </content>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)
        regdown = self.parser.get_regdown_for_paragraph(paragraph_node)
        self.assertIn('![image alt](https:///images/image_name.png)', regdown)

    def test_regdown_paragraph_with_table(self):
        regml = b'''
            <paragraph xmlns="eregs" label="1010-A-III-h8-p34" marker="">
                <content>
                    <table>
                        <header>
                            <columnHeaderRow>
                                <column colspan="1" rowspan="2"/>
                                <column colspan="2" rowspan="1">
                                    Name
                                </column>
                            </columnHeaderRow>
                        </header>
                        <row>
                            <cell>Water</cell>
                        </row>
                    </table>
                </content>
            </paragraph>'''
        paragraph_node = etree.fromstring(regml)
        regdown = self.parser.get_regdown_for_paragraph(paragraph_node)
        self.assertIn('<th scope="col" rowspan="2" colspan="1"/>', regdown)
        self.assertIn('<td align="left">Water</td>', regdown)
        self.assertIn('<thead>', regdown)
        self.assertIn('<tbody>', regdown)

# -*- coding: utf-8 -*-
import datetime
import json
import unittest
from unittest import mock

from django.conf import settings
from django.test import TestCase as DjangoTestCase

from bs4 import BeautifulSoup as bS
from requests import Response

from regulations3k.models import Part, Subpart
from regulations3k.parser import paragraphs
from regulations3k.parser.integer_conversion import (
    alpha_to_int,
    int_to_alpha,
    int_to_roman,
    roman_to_int,
)
from regulations3k.parser.patterns import IdLevelState
from regulations3k.parser.regtable import RegTable
from regulations3k.scripts import ecfr_importer
from regulations3k.scripts.ecfr_importer import PAYLOAD, divine_interp_tag_use


class RegTableTestCase(unittest.TestCase):
    def test_regtable_id(self):
        reg_table = RegTable("1-a")
        self.assertEqual(reg_table.label, "1-a")


class ImporterTestCase(DjangoTestCase):
    """Tests for section and appendix parsing."""

    fixtures = ["test_parts.json"]
    # xml_fixture has partial XML for regs 1002 and 1005
    xml_fixture = "{}/regulations3k/fixtures/graftest.xml".format(settings.PROJECT_ROOT)
    interp_fixture = "{}/regulations3k/fixtures/interptest.xml".format(
        settings.PROJECT_ROOT
    )
    with open(xml_fixture, "r") as f:
        test_xml = f.read()
    with open(interp_fixture, "r") as f:
        interp_xml = f.read()

    def test_appendix_id_type_sniffer(self):
        ls = IdLevelState()
        p_soup = bS(self.test_xml, "lxml-xml")
        appendices = p_soup.find_all("DIV5")[1].find_all("DIV9")
        appendix_0_graphs = appendices[0].find_all("P")
        appendix_0_type = ls.sniff_appendix_id_type(appendix_0_graphs)
        self.assertEqual("appendix", appendix_0_type)
        appendix_1_graphs = appendices[1].find_all("P")
        appendix_1_type = ls.sniff_appendix_id_type(appendix_1_graphs)
        self.assertEqual("section", appendix_1_type)
        appendix_2_graphs = appendices[2].find_all("P")
        appendix_2_type = ls.sniff_appendix_id_type(appendix_2_graphs)
        self.assertIs(appendix_2_type, None)

    def test_appendix_graph_parsing(self):
        ls = IdLevelState()
        p_soup = bS(self.test_xml, "lxml-xml")
        graphs = p_soup.find_all("DIV5")[1].find_all("DIV9")[1].find_all("P")
        parsed_graph2 = ls.parse_appendix_graph(graphs[2], "1002-A")
        self.assertIn("(2) To the extent not included in item 1 above:", parsed_graph2)
        parsed_graph3 = ls.parse_appendix_graph(graphs[3], "1002-A")
        self.assertIn("(i) National banks", parsed_graph3)
        ecfr_importer.parse_appendix_paragraphs(graphs, "appendix", "1002-A")
        self.assertIn("\n1(a)", p_soup.text)

    def test_interp_graph_parsing(self):
        soup = bS(self.interp_xml, "lxml-xml")
        part_soup = soup.find("DIV5")
        PAYLOAD.parse_part(part_soup, "1002")
        part = PAYLOAD.part
        PAYLOAD.parse_version(part_soup, part)
        version = PAYLOAD.version
        interp_subpart = Subpart(
            title="Supplement I to Part {}".format(part.part_number),
            label="Official Interpretations",
            version=version,
        )
        interp_subpart.save()
        interp = [
            div
            for div in part_soup.find_all("DIV9")
            if div.find("HEAD").text.startswith("Supplement I")
        ][0]
        ecfr_importer.parse_interps(interp, part, interp_subpart)
        self.assertEqual(
            Subpart.objects.filter(title__contains="Supplement I").count(),
            1,
        )

    def test_parse_appendix_elements(self):
        p_soup = bS(self.test_xml, "lxml-xml")
        appendix = p_soup.find("DIV5").find("DIV9")
        parsed_appendix = ecfr_importer.parse_appendix_elements(appendix, "A")
        self.assertIn("**1.", parsed_appendix)

    def test_parse_appendix_elements_with_interp_ref(self):
        PAYLOAD.interp_refs.update({"A": {"1": "see(A-1-Interp)"}})
        p_soup = bS(self.test_xml, "lxml-xml")
        appendix = p_soup.find("DIV5").find("DIV9")
        parsed_appendix = ecfr_importer.parse_appendix_elements(appendix, "A")
        self.assertIn("{1}", parsed_appendix)
        self.assertIn("(print or type):__", parsed_appendix)
        self.assertIn("<table>", parsed_appendix)
        self.assertIn("![image-A-1]", parsed_appendix)
        self.assertIn("{table-A-0}", PAYLOAD.tables.keys())

    def test_set_table(self):
        PAYLOAD.reset()
        p_soup = bS(self.test_xml, "lxml-xml")
        appendix = p_soup.find("DIV5").find("DIV9")
        table = appendix.find("TABLE")
        table_id = "table-A-0"
        ecfr_importer.set_table(table, table_id)
        self.assertIn(table_id, PAYLOAD.tables.keys())
        self.assertTrue(isinstance(PAYLOAD.tables[table_id], RegTable))

    def test_table_no_head_rows(self):
        test_table = (
            "<DIV>\n"
            '<TABLE class="gpotbl_table">\n'
            "<TR>\n"
            "<TD>\n"
            "Cell content\n"
            "</TD>\n"
            "</TR>"
            "</TABLE>"
            "</DIV>"
        )
        table_soup = bS(test_table, "lxml-xml").find("TABLE")
        table_label = "{table-test-label}"
        regtable = RegTable(table_label)
        msg = regtable.parse_xml_table(table_soup)
        self.assertEqual(msg, "Table is set for {}!".format(table_label))
        self.assertNotIn("<thead>", regtable.table())

    @mock.patch("regulations3k.scripts.ecfr_importer.requests.get")
    def test_parser_good_request(self, mock_get):
        part_number = "1002"
        mock_response = mock.Mock(
            Response, ok=True, text=self.test_xml, encoding="utf-8"
        )
        mock_get.return_value = mock_response
        mock_response.json.return_value = json.loads(
            '{"results": [{"effective_on": "2018-01-01"}]}'
        )
        ecfr_importer.ecfr_to_regdown(part_number)
        self.assertEqual(mock_get.call_count, 2)

    @mock.patch("regulations3k.parser.payload.requests.get")
    def test_good_effective_date_request(self, mock_get):
        mock_response = mock.Mock(Response, ok=True)
        mock_response.json.return_value = json.loads(
            '{"results": [{"effective_on": "2018-01-01"}]}'
        )
        mock_get.return_value = mock_response
        PAYLOAD.get_effective_date("1002")
        self.assertEqual(PAYLOAD.effective_date, datetime.date(2018, 1, 1))

    @mock.patch("regulations3k.parser.payload.requests.get")
    def test_bad_effective_date_request_returns_none(self, mock_get):
        mock_response = mock.Mock(Response, ok=False)
        mock_get.return_value = mock_response
        PAYLOAD.get_effective_date("1002")
        self.assertIs(PAYLOAD.effective_date, None)

    @mock.patch("regulations3k.scripts.ecfr_importer.requests.get")
    def test_failed_parser_request_returns_none(self, mock_get):
        mock_response = mock.Mock(
            Response,
            reason="REQUESTS FOR HUMANS MY EYE",
            status_code=404,
            ok=False,
        )
        mock_get.return_value = mock_response
        self.assertIs(ecfr_importer.ecfr_to_regdown("1002"), None)
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch("regulations3k.scripts.ecfr_importer.requests.get")
    def test_part_parser_uses_existing(self, mock_get):
        mock_response = mock.Mock(  # mock to skip the effective_date request
            Response,
            reason="REQUESTS FOR HUMANS MY EYE",
            status_code=404,
            ok=False,
        )
        mock_get.return_value = mock_response
        part_number = "1003"  # This part exists in the loaded fixture
        ecfr_importer.ecfr_to_regdown(part_number, file_path=self.xml_fixture)
        self.assertEqual(Part.objects.filter(part_number=part_number).count(), 1)

    @mock.patch("regulations3k.scripts.ecfr_importer.requests.get")
    def test_part_parser_create_new(self, mock_get):
        """Check that a regulation part that isn't loaded gets created."""
        part_number = "1002"  # This part does not exist in the loaded fixture
        mock_response = mock.Mock(  # mock the effective_date request
            Response, reason="REQUESTS FOR HUMANS MY EYE", ok=True
        )
        mock_response.json.return_value = {"results": [{"effective_on": "2018-06-01"}]}
        mock_get.return_value = mock_response
        ecfr_importer.ecfr_to_regdown(part_number, file_path=self.xml_fixture)
        self.assertEqual(Part.objects.filter(part_number=part_number).count(), 1)

    def test_bad_file_path_returns_none(self):
        self.assertIs(
            ecfr_importer.ecfr_to_regdown("1002", file_path="fake_file_path"),
            None,
        )
        self.assertEqual(Part.objects.filter(part_number="1002").count(), 0)

    def test_interp_inferred_section_graph_parsing(self):
        PAYLOAD.reset()
        self.assertEqual(PAYLOAD.interp_refs, {})
        soup = bS(self.interp_xml, "lxml-xml")
        parts = soup.find_all("DIV5")
        part_soup = [div for div in parts if div["N"] == "1030"][0]
        PAYLOAD.parse_part(part_soup, "1030")
        part = PAYLOAD.part
        PAYLOAD.parse_version(part_soup, part)
        version = PAYLOAD.version
        interp_subpart = Subpart(
            title="Supplement I to Part {}".format(part.part_number),
            label="Official Interpretations",
            version=version,
        )
        interp_subpart.save()
        interp = [
            div
            for div in part_soup.find_all("DIV9")
            if div.find("HEAD").text.startswith("Supplement I")
        ][0]
        ecfr_importer.parse_interps(interp, part, interp_subpart)
        self.assertEqual(PAYLOAD.interp_refs["1"]["c"], "see(1-c-Interp)")


class AppendixCreationTestCase(DjangoTestCase):
    """Checks that parse_appendices() creates objects as expected."""

    fixtures = ["tree_limb.json"]
    xml_fixture = "{}/regulations3k/fixtures/graftest.xml".format(settings.PROJECT_ROOT)
    with open(xml_fixture, "r") as f:
        test_xml = f.read()

    def test_parse_appendices_no_appendix(self):
        self.assertIs(ecfr_importer.parse_appendices("", {}), None)

    def test_parse_appendices_creation(self):
        PAYLOAD.reset()
        self.assertEqual(len(PAYLOAD.appendices), 0)
        test_part = Part.objects.first()
        test_subpart = Subpart.objects.first()
        PAYLOAD.subparts["appendix_subpart"] = test_subpart
        PAYLOAD.interp_refs.update({"A": {"1": "see(A-1-Interp)"}})
        soup = bS(self.test_xml, "lxml-xml")
        test_appendices = [soup.find("DIV5").find("DIV9")]
        ecfr_importer.parse_appendices(test_appendices, test_part)
        self.assertEqual(len(PAYLOAD.appendices), 1)


class AppendixNamingTestCase(unittest.TestCase):
    """Tests for the naming of appendices."""

    def test_get_appendix_label_default(self):
        self.assertEqual(
            ecfr_importer.get_appendix_label("", "unhelpful head", "Z"), "Z"
        )

    def test_get_appendix_label_good_N_value(self):
        self.assertEqual(
            ecfr_importer.get_appendix_label("Appendix X", "unhelpful head", "Z"),
            "X",
        )

    def test_get_appendix_label_no_N_value(self):
        self.assertEqual(
            ecfr_importer.get_appendix_label("", "Appendix X to Reg 1030", "Z"),
            "X",
        )

    def test_get_appendix_label_appendices(self):
        self.assertEqual(
            ecfr_importer.get_appendix_label("", "Appendices G and H to Reg 1030", "Z"),
            "GH",
        )

    def test_get_appendix_label_appendixes(self):
        self.assertEqual(
            ecfr_importer.get_appendix_label("", "Appendixes G and H to Reg 1030", "Z"),
            "GH",
        )


class ImporterRunTestCase(unittest.TestCase):
    """Tests for running the ecfr importer via commands."""

    @mock.patch("regulations3k.scripts.ecfr_importer.ecfr_to_regdown")
    def test_run_with_one_arg_calls_importer(self, mock_importer):
        ecfr_importer.run("1002")
        self.assertEqual(mock_importer.call_count, 1)

    @mock.patch("regulations3k.scripts.ecfr_importer.ecfr_to_regdown")
    def test_run_works_with_local_file(self, mock_importer):
        ecfr_importer.run("1002", "/mock/local/file.xml")
        self.assertEqual(mock_importer.call_count, 1)

    @mock.patch("regulations3k.scripts.ecfr_importer.ecfr_to_regdown")
    def test_run_all(self, mock_importer):
        ecfr_importer.run("ALL")
        self.assertEqual(mock_importer.call_count, 11)

    @mock.patch("regulations3k.scripts.ecfr_importer.ecfr_to_regdown")
    def test_run_all_with_local_file(self, mock_importer):
        ecfr_importer.run("ALL", "/mock/local/file.xml")
        self.assertEqual(mock_importer.call_count, 11)

    def test_run_importer_no_args(self):
        with self.assertRaises(SystemExit):
            ecfr_importer.run()

    def test_run_importer_non_cfpb_part_args(self):
        """The Part number must be on our allowlist"""
        with self.assertRaises(ValueError):
            ecfr_importer.run("9999")
        with self.assertRaises(ValueError):
            ecfr_importer.run("DROP TABLE")


class ParagraphParsingTestCase(unittest.TestCase):
    fixtures_dir = "{}/regulations3k/fixtures".format(settings.PROJECT_ROOT)
    # test paragraphs are from reg DD, section 1030.4
    test_paragraph_xml_path = "{}/test_graphs_with_multi_ids.xml".format(fixtures_dir)
    with open(test_paragraph_xml_path, "r") as f:
        test_xml = f.read()
    LEVEL_STATE = IdLevelState()

    def test_paragraph_bold_linting(self):
        test_graph = "Now is the time to **See** the best **et seq.** ever."
        expected_result = "Now is the time to *See* the best *et seq.* ever."
        result = paragraphs.lint_paragraph(test_graph)
        self.assertEqual(result, expected_result)

    def test_paragraph_bold_linting_insensitive_sic(self):
        test_graph = "Now is the time to **see** the best **Et. seq.** ever."
        expected_result = "Now is the time to *see* the best *Et. seq.* ever."
        result = paragraphs.lint_paragraph(test_graph)
        self.assertEqual(result, expected_result)

    def test_paragraph_emdash_linting(self):
        test_graph = "Now is the time -\n"
        expected_result = "Now is the time ---\n"
        result = paragraphs.lint_paragraph(test_graph)
        self.assertEqual(result, expected_result)

    def test_singleton_parsing_invalid_tag(self):
        graph = "A graf with (or) as a potential but invalid ID."
        parsed_graph = ecfr_importer.parse_singleton_graph(graph, "1")
        self.assertEqual(parsed_graph, "\n" + graph + "\n")

    def test_multi_id_paragraph_parsing(self):
        soup = bS(self.test_xml, "lxml-xml")
        graph_soup = soup.find_all("P")
        parsed_graphs = ecfr_importer.parse_section_paragraphs(graph_soup, "1")
        self.assertIn("**(a) Delivery of account disclosures**", parsed_graphs)

    def test_multi_id_paragraph_parsing_with_interp_reference(self):
        PAYLOAD.interp_refs.update(
            {
                "2": {
                    "p": "see(2-p-Interp)",
                    "p-1": "see(2-p-1-Interp)",
                    "p-1-i": "see(2-p-1-i-Interp)",
                }
            }
        )
        graph = (
            "<P>(p) <I>Empirically derived scoring systems</I> - "
            "(1) <I>Credit scoring systems</I> (i) Credit scoring systems "
            "evaluate an applicant's creditworthiness mechanically.\n</P>"
        )
        result = ecfr_importer.parse_multi_id_graph(graph, ["p", "1", "i"], "2")
        self.assertIn("see(2-p-1-i-Interp)", result)

    def test_multiple_id_test_true(self):
        ls = self.LEVEL_STATE
        self.assertTrue(ls.multiple_id_test(["a", "1"]))
        self.assertFalse(ls.multiple_id_test(["a", "i"]))
        self.assertTrue(ls.multiple_id_test(["1", "i"]))
        self.assertFalse(ls.multiple_id_test(["1", "b"]))
        self.assertTrue(ls.multiple_id_test(["i", "A"]))
        self.assertFalse(ls.multiple_id_test(["ii", "B"]))
        self.assertTrue(ls.multiple_id_test(["A", "1"]))
        self.assertFalse(ls.multiple_id_test(["B", "2"]))

    @mock.patch("regulations3k.scripts.ecfr_importer.parse_multi_id_graph")
    def test_three_passing_ids(self, mock_parser):
        test_graph = "(a) text (1) text (i) text."
        three_good_ids = ["a", "1", "i"]
        ecfr_importer.parse_ids(test_graph, "1002-1")
        mock_parser.assert_called_with(test_graph, three_good_ids, "1002-1")

    @mock.patch("regulations3k.scripts.ecfr_importer.parse_multi_id_graph")
    def test_two_passing_ids(self, mock_parser):
        test_graph = "(a) text (1) text (b) text."
        two_good_ids = ["a", "1"]
        ecfr_importer.parse_ids(test_graph, "1002-1")
        mock_parser.assert_called_with(test_graph, two_good_ids, "1002-1")

    def test_parse_interp_graph_reference(self):
        valid_graph_element = bS("<HD3>Paragraph 2(c)(1)</HD3>", "lxml-xml")
        self.assertEqual(
            ecfr_importer.parse_interp_graph_reference(
                valid_graph_element, "1002", "2"
            ),
            "2-c-1-Interp",
        )
        invalid_graph_element = bS("<HD3>Paragraph X(5)(a)</HD3>", "lxml-xml")
        self.assertEqual(
            ecfr_importer.parse_interp_graph_reference(
                invalid_graph_element, "1002", "2"
            ),
            "",
        )
        valid_inferred_section_graph_element = bS(
            "<HD3>Paragraph (c)(1)</HD3>", "lxml-xml"
        )
        self.assertEqual(
            ecfr_importer.parse_interp_graph_reference(
                valid_inferred_section_graph_element, "1030", "2"
            ),
            "2-c-1-Interp",
        )

    def test_parse_interp_graph_no_id(self):
        section_graph_element_no_id = bS(
            "<P>This is a bare interp paragraph with no ID.</P>", "lxml-xml"
        )
        parsed_graph = ecfr_importer.parse_interp_graph(section_graph_element_no_id)
        self.assertTrue(parsed_graph.startswith("This is a bare interp"))

    def test_get_interp_section_tag(self):
        headline = "Section 1003.2 - Definitions"
        self.assertEqual(ecfr_importer.get_interp_section_tag(headline), "2")
        headline = "\xa7 1003.2 - Definitions"
        self.assertEqual(ecfr_importer.get_interp_section_tag(headline), "2")
        headline = "Appendix A - Model Disclosure Clauses and Forms"
        self.assertEqual(ecfr_importer.get_interp_section_tag(headline), "A")
        headline = "Appendices G and H - A dreaded Combo Appendix Section"
        self.assertEqual(ecfr_importer.get_interp_section_tag(headline), "GH")
        headline = "Introduction"
        self.assertEqual(ecfr_importer.get_interp_section_tag(headline), "0")
        headline = "Appendix MS-3 - Model Force-Placed Insurance Notice Forms"
        self.assertEqual(ecfr_importer.get_interp_section_tag(headline), "MS3")
        headline = "Inevitable - Random Section Name"
        self.assertEqual(ecfr_importer.get_interp_section_tag(headline), "Inevitable")

    def test_divine_interp_tag(self):

        # HD1 elements
        HD = bS("<HD1>Introduction\n</HD1>", "lxml-xml").find("HD1")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "intro")
        HD = bS("<HD1>Appendix X - X-rays\n</HD1>", "lxml-xml").find("HD1")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "appendix")
        HD = bS("<HD1>Appendices G & H - Cane\n</HD1>", "lxml-xml").find("HD1")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "appendices")
        HD = bS("<HD1>Section 1002.4 - Known\n</HD1>", "lxml-xml").find("HD1")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "section")
        HD = bS("<HD1>Inevitable Random HD1\n</HD1>", "lxml-xml").find("HD1")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "")
        # HD2 elements
        HD = bS("<HD2>Section 1002.4 - Known\n</HD2>", "lxml-xml").find("HD2")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "section")
        HD = bS("<HD2>2(b) Application\n</HD2>", "lxml-xml").find("HD2")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "graph_id")
        # HD3 elements
        HD = bS("<HD3>Section 1002.4 - Known\n</HD3>", "lxml-xml").find("HD3")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "section")
        HD = bS("<HD3>2(b) Application\n</HD3>", "lxml-xml").find("HD3")
        self.assertEqual(divine_interp_tag_use(HD, "1002"), "graph_id")
        HD = bS("<HD3>(b) Application\n</HD3>", "lxml-xml").find("HD3")
        self.assertEqual(divine_interp_tag_use(HD, "1030"), "graph_id_inferred_section")


class ParserIdTestCase(unittest.TestCase):

    LEVEL_STATE = IdLevelState()

    def test_current_token(self):
        ls = self.LEVEL_STATE
        ls.current_id = "2-a-1-i-Interp-2-ii"
        self.assertEqual(ls.current_token(), "ii")
        ls.current_id = "a-5-ii-A"
        self.assertEqual(ls.current_token(), "A")

    def test_roman_test_invalid_level(self):
        self.LEVEL_STATE.current_id = "a"
        self.assertFalse(self.LEVEL_STATE.roman_test("ii"))

    def test_multiple_id_test_level_2_passes(self):
        self.LEVEL_STATE.current_id = "a-1"
        ids = ["2", "i", "A"]
        self.assertTrue(self.LEVEL_STATE.multiple_id_test(ids))

    def test_multiple_id_test_level_3_passes(self):
        self.LEVEL_STATE.current_id = "a-1-i"
        ids = ["ii", "A", "1"]
        self.assertTrue(self.LEVEL_STATE.multiple_id_test(ids))

    def test_token_validity_test_true(self):
        ls = self.LEVEL_STATE
        self.assertTrue(ls.token_validity_test("a"))
        self.assertTrue(ls.token_validity_test("aa"))
        self.assertTrue(ls.token_validity_test("1"))
        self.assertTrue(ls.token_validity_test("i"))
        self.assertTrue(ls.token_validity_test("iv"))
        self.assertTrue(ls.token_validity_test("B"))
        self.assertTrue(ls.token_validity_test("BB"))

    def test_token_validity_test_false(self):
        ls = self.LEVEL_STATE
        self.assertFalse(ls.token_validity_test("ab"))
        self.assertFalse(ls.token_validity_test("<"))
        self.assertFalse(ls.token_validity_test("."))

    def test_next_interp_ids(self):
        """Testing the interp pattern [pid]-Interp-1-i-A"""
        ls = self.LEVEL_STATE
        # initializes with next token
        ls.current_id = ""
        ls.next_token = "2-a-1-i-Interp"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp")
        self.assertEqual(ls.interp_level(), 1)

        # surf level 1
        ls.current_id = "2-a-1-i-Interp"
        ls.next_token = "1"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-1")
        self.assertEqual(ls.interp_level(), 1)
        # surf
        ls.next_token = "2"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-2")
        # dive
        ls.next_token = "i"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-2-i")
        # dive
        ls.next_token = "A"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-2-i-A")
        # surf level 3
        ls.next_token = "B"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-2-i-B")
        # rise
        ls.next_token = "ii"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-2-ii")
        # rise
        ls.next_token = "3"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-3")
        # rise 2
        ls.current_id = "2-a-1-i-Interp-2-ii-A"
        ls.next_token = "3"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-3")
        # roman surf
        ls.current_id = "2-a-1-i-Interp-2-iii"
        ls.next_token = "iv"
        self.assertEqual(ls.next_interp_id(), "2-a-1-i-Interp-2-iv")

    def test_next_appendix_ids(self):
        """Testing the appendix pattern 1-i-A"""
        ls = self.LEVEL_STATE
        # initializes with next token
        ls.current_id = ""
        ls.next_token = "1"
        self.assertEqual(ls.next_appendix_id(), "1")
        # surf level 1
        ls.current_id = "1"
        ls.next_token = "2"
        self.assertEqual(ls.next_appendix_id(), "2")
        # dive
        ls.next_token = "i"
        self.assertEqual(ls.next_appendix_id(), "2-i")
        # surf level 2
        ls.next_token = "ii"
        self.assertEqual(ls.next_appendix_id(), "2-ii")
        # dive
        ls.next_token = "A"
        self.assertEqual(ls.next_appendix_id(), "2-ii-A")
        # surf level 3
        ls.next_token = "B"
        self.assertEqual(ls.next_appendix_id(), "2-ii-B")
        # rise
        ls.next_token = "iii"
        self.assertEqual(ls.next_appendix_id(), "2-iii")
        # rise
        ls.next_token = "3"
        self.assertEqual(ls.next_appendix_id(), "3")
        # rise 2
        ls.current_id = "1-i-A"
        ls.next_token = "2"
        self.assertEqual(ls.next_appendix_id(), "2")

    def test_next_appendix_id_1a(self):
        """Testing the appendix/interp-intro pattern 1-a."""
        ls = self.LEVEL_STATE
        # initializes with next token
        ls.current_id = ""
        ls.next_token = "1"
        self.assertEqual(ls.next_appendix_id_1a(), "1")
        # surf level 1
        ls.current_id = "1"
        ls.next_token = "2"
        self.assertEqual(ls.next_appendix_id_1a(), "2")
        # dive
        ls.next_token = "a"
        self.assertEqual(ls.next_appendix_id_1a(), "2-a")
        # surf level 2
        ls.next_token = "b"
        self.assertEqual(ls.next_appendix_id_1a(), "2-b")
        # rise
        ls.next_token = "3"
        self.assertEqual(ls.next_appendix_id_1a(), "3")


class PatternsTestCase(unittest.TestCase):

    levelstate = IdLevelState()

    def test_appendix_level_1_initial(self):
        """Testing the appendix indentation pattern 1-i-A"""
        self.levelstate.current_id = ""
        self.levelstate.next_token = "1"
        self.assertEqual(self.levelstate.next_appendix_id(), "1")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "1")

    def test_appendix_level_1_surf(self):
        self.levelstate.current_id = "1"
        self.levelstate.next_token = "2"
        self.assertEqual(self.levelstate.next_appendix_id(), "2")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "2")

    def test_appendix_level_1_dive(self):
        self.levelstate.current_id = "1"
        self.levelstate.next_token = "i"
        self.assertEqual(self.levelstate.next_appendix_id(), "1-i")
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), "i")

    def test_appendix_level_2_surf(self):
        self.levelstate.current_id = "1-i"
        self.levelstate.next_token = "ii"
        self.assertEqual(self.levelstate.next_appendix_id(), "1-ii")
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), "ii")

    def test_appendix_level_2_rise(self):
        self.levelstate.current_id = "1-i"
        self.levelstate.next_token = "2"
        self.assertEqual(self.levelstate.next_appendix_id(), "2")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "2")

    def test_level_1_initial(self):
        self.levelstate.current_id = ""
        self.levelstate.next_token = "a"
        self.assertEqual(self.levelstate.next_id(), "a")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "a")

    def test_level_1_dive(self):
        self.levelstate.current_id = "b"
        self.levelstate.next_token = "1"
        self.assertEqual(self.levelstate.next_id(), "b-1")
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), "1")

    def test_level_2_surf(self):
        self.levelstate.current_id = "a-1"
        self.levelstate.next_token = "2"
        self.assertEqual(self.levelstate.next_id(), "a-2")
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), "2")

    def test_level_2_dive(self):
        self.levelstate.current_id = "e-3"
        self.levelstate.next_token = "i"
        self.assertEqual(self.levelstate.next_id(), "e-3-i")
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), "i")

    def test_level_2_rise(self):
        self.levelstate.current_id = "e-3"
        self.levelstate.next_token = "f"
        self.assertEqual(self.levelstate.next_id(), "f")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "f")

    def test_level_3_surf(self):
        self.levelstate.current_id = "a-3-ii"
        self.levelstate.next_token = "iii"
        self.assertEqual(self.levelstate.next_id(), "a-3-iii")
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), "iii")

    def test_level_3_dive(self):
        self.levelstate.current_id = "d-4-iv"
        self.levelstate.next_token = "A"
        self.assertEqual(self.levelstate.next_id(), "d-4-iv-A")
        self.assertEqual(self.levelstate.level(), 4)
        self.assertEqual(self.levelstate.current_token(), "A")

    def test_level_3_rise(self):
        self.levelstate.current_id = "a-3-ii"
        self.levelstate.next_token = "4"
        self.assertEqual(self.levelstate.next_id(), "a-4")
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), "4")

    def test_level_3_rise_2(self):
        self.levelstate.current_id = "a-3-ii"
        self.levelstate.next_token = "b"
        self.assertEqual(self.levelstate.next_id(), "b")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "b")

    def test_level_4_surf(self):
        self.levelstate.current_id = "a-3-ii-A"
        self.levelstate.next_token = "B"
        self.assertEqual(self.levelstate.next_id(), "a-3-ii-B")
        self.assertEqual(self.levelstate.level(), 4)
        self.assertEqual(self.levelstate.current_token(), "B")

    def test_level_4_dive(self):
        self.levelstate.current_id = "d-4-iv-A"
        self.levelstate.next_token = "1"
        self.assertEqual(self.levelstate.next_id(), "d-4-iv-A-1")
        self.assertEqual(self.levelstate.level(), 5)
        self.assertEqual(self.levelstate.current_token(), "1")

    def test_level_4_rise(self):
        self.levelstate.current_id = "a-3-ii-A"
        self.levelstate.next_token = "iii"
        self.assertEqual(self.levelstate.next_id(), "a-3-iii")
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), "iii")

    def test_level_4_rise_2(self):
        self.levelstate.current_id = "a-3-ii-A"
        self.levelstate.next_token = "4"
        self.assertEqual(self.levelstate.next_id(), "a-4")
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), "4")

    def test_level_4_rise_3(self):
        self.levelstate.current_id = "a-3-ii-A"
        self.levelstate.next_token = "b"
        self.assertEqual(self.levelstate.next_id(), "b")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "b")

    def test_level_5_surf(self):
        self.levelstate.current_id = "a-3-ii-A-1"
        self.levelstate.next_token = "2"
        self.assertEqual(self.levelstate.next_id(), "a-3-ii-A-2")
        self.assertEqual(self.levelstate.level(), 5)
        self.assertEqual(self.levelstate.current_token(), "2")

    def test_level_5_dive(self):
        self.levelstate.current_id = "a-3-ii-A-2"
        self.levelstate.next_token = "i"
        self.assertEqual(self.levelstate.next_id(), "a-3-ii-A-2-i")
        self.assertEqual(self.levelstate.level(), 6)
        self.assertEqual(self.levelstate.current_token(), "i")

    def test_level_5_rise(self):
        self.levelstate.current_id = "a-3-ii-A-1"
        self.levelstate.next_token = "B"
        self.assertEqual(self.levelstate.next_id(), "a-3-ii-B")
        self.assertEqual(self.levelstate.level(), 4)
        self.assertEqual(self.levelstate.current_token(), "B")

    def test_level_5_rise_2(self):
        self.levelstate.current_id = "a-3-ii-A-1"
        self.levelstate.next_token = "iii"
        self.assertEqual(self.levelstate.next_id(), "a-3-iii")
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), "iii")

    def test_level_5_rise_3(self):
        self.levelstate.current_id = "a-3-ii-A-1"
        self.levelstate.next_token = "4"
        self.assertEqual(self.levelstate.next_id(), "a-4")
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), "4")

    def test_level_5_rise_4(self):
        self.levelstate.current_id = "a-3-ii-A-1"
        self.levelstate.next_token = "b"
        self.assertEqual(self.levelstate.next_id(), "b")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "b")

    def test_level_6_surf(self):
        self.levelstate.current_id = "a-3-ii-A-1-iv"
        self.levelstate.next_token = "v"
        self.assertEqual(self.levelstate.next_id(), "a-3-ii-A-1-v")
        self.assertEqual(self.levelstate.level(), 6)
        self.assertEqual(self.levelstate.current_token(), "v")

    def test_level_6_rise(self):
        self.levelstate.current_id = "a-3-ii-A-1-iv"
        self.levelstate.next_token = "2"
        self.assertEqual(self.levelstate.next_id(), "a-3-ii-A-2")
        self.assertEqual(self.levelstate.level(), 5)
        self.assertEqual(self.levelstate.current_token(), "2")

    def test_level_6_rise_2(self):
        self.levelstate.current_id = "a-3-ii-A-1-iv"
        self.levelstate.next_token = "B"
        self.assertEqual(self.levelstate.next_id(), "a-3-ii-B")
        self.assertEqual(self.levelstate.level(), 4)
        self.assertEqual(self.levelstate.current_token(), "B")

    def test_level_6_rise_3(self):
        self.levelstate.current_id = "a-3-ii-A-1-iv"
        self.levelstate.next_token = "iii"
        self.assertEqual(self.levelstate.next_id(), "a-3-iii")
        self.assertEqual(self.levelstate.level(), 3)
        self.assertEqual(self.levelstate.current_token(), "iii")

    def test_level_6_rise_4(self):
        self.levelstate.current_id = "a-3-ii-A-1-iv"
        self.levelstate.next_token = "4"
        self.assertEqual(self.levelstate.next_id(), "a-4")
        self.assertEqual(self.levelstate.level(), 2)
        self.assertEqual(self.levelstate.current_token(), "4")

    def test_level_6_rise_5(self):
        self.levelstate.current_id = "a-3-ii-A-1-iv"
        self.levelstate.next_token = "b"
        self.assertEqual(self.levelstate.next_id(), "b")
        self.assertEqual(self.levelstate.level(), 1)
        self.assertEqual(self.levelstate.current_token(), "b")

    def test_level_6_bad_previous_digit(self):
        self.levelstate.current_id = "a-3-ii-A-a-iv"
        self.levelstate.next_token = "v"
        self.assertEqual(self.levelstate.next_id(), "a-3-ii-A-a-v")

    def test_roman_surf_test_level_3_token_not_roman(self):
        self.levelstate.current_id = "a-1-1"
        self.assertIs(
            self.levelstate.roman_surf_test(self.levelstate.current_token, "ii"),
            False,
        )

    def test_roman_surf_test_true(self):
        self.levelstate.current_id = "a-1-i"
        self.assertIs(
            self.levelstate.roman_surf_test(self.levelstate.current_token(), "ii"),
            True,
        )

    def test_roman_surf_test_false_if_blank_token(self):
        self.levelstate.current_id = ""
        self.assertIs(
            self.levelstate.roman_surf_test(self.levelstate.current_token(), "ii"),
            False,
        )

    def test_alpha_surf_test(self):
        self.assertIs(self.levelstate.alpha_surf_test("a", "b"), True)

    def test_alpha_surf_test_non_alpha(self):
        self.assertIs(self.levelstate.alpha_surf_test("1", "b"), False)

    def test_alpha_surf_test_not_next_alpha(self):
        self.assertIs(self.levelstate.alpha_surf_test("a", "c"), False)

    def test_alpha_surf_test_not_same_case(self):
        self.assertIs(self.levelstate.alpha_surf_test("a", "C"), False)

    def test_root_token(self):
        self.levelstate.current_id = "a-1-i"
        self.assertEqual(self.levelstate.root_token(), "a")


class EtruscanTestCase(unittest.TestCase):
    """Testing the Roman functions"""

    tokens = {
        "i": 1,
        "ii": 2,
        "iii": 3,
        "iv": 4,
        "v": 5,
        "vi": 6,
        "vii": 7,
        "viii": 8,
        "ix": 9,
        "x": 10,
        "xi": 11,
        "xl": 40,
        "l": 50,
        "c": 100,
    }

    def test_roman_to_int(self):
        for token in self.tokens:
            self.assertEqual(roman_to_int(token), self.tokens[token])

    def test_int_to_roman(self):
        for key, value in self.tokens.items():
            self.assertEqual(int_to_roman(value), key)

    def test_int_to_roman_invalid_type(self):
        self.assertIs(roman_to_int(1), None)

    def test_int_to_roman_invalid_sequence(self):
        self.assertIs(roman_to_int("ic"), None)

    def test_int_to_roman_non_integer(self):
        with self.assertRaises(TypeError):
            int_to_roman("A")

    def test_int_to_roman_out_of_range(self):
        with self.assertRaises(ValueError):
            int_to_roman(4000)

    def test_alpha_to_int(self):
        self.assertIs(alpha_to_int(1), None)
        self.assertIs(alpha_to_int("a-3"), None)
        self.assertIs(alpha_to_int(3.14), None)
        self.assertIs(alpha_to_int("aA"), None)
        self.assertEqual(alpha_to_int("a"), 1)
        self.assertEqual(alpha_to_int("Z"), 26)
        self.assertEqual(alpha_to_int("aa"), 27)
        self.assertEqual(alpha_to_int("ZZ"), 52)

    def test_int_to_alpha(self):
        self.assertIs(int_to_alpha("a"), None)
        self.assertIs(int_to_alpha(3.14), None)
        self.assertIs(int_to_alpha(-1), None)
        self.assertEqual(int_to_alpha(1), "a")
        self.assertEqual(int_to_alpha(26), "z")
        self.assertEqual(int_to_alpha(27), "aa")
        self.assertEqual(int_to_alpha(30), "dd")
        self.assertEqual(int_to_alpha(52), "zz")
        self.assertIs(int_to_alpha(53), None)

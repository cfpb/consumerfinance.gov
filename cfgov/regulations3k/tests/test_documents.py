from unittest import TestCase

from regulations3k.documents import SectionParagraphDocument
from regulations3k.models import (
    EffectiveVersion, Part, Section, SectionParagraph, Subpart
)


class SectionParagraphDocumentTest(TestCase):

    def test_prepare(self):
        part = Part(cfr_title_number="0001",
                    chapter="1",
                    part_number="1234",
                    title="Test Title",
                    short_name="short name")
        version = EffectiveVersion(authority="authority",
                                   source="Source",
                                   part=part)
        subpart = Subpart(label="Subpart Label",
                          title="Subpart Title",
                          version=version)
        section = Section(label="Section Label",
                          title="Section Title",
                          subpart=subpart,
                          sortable_label="Sortable Label")
        section_paragraph = SectionParagraph(paragraph="Paragraph",
                                             paragraph_id="1",
                                             section=section)

        doc = SectionParagraphDocument()

        prepared_data = doc.prepare(section_paragraph)
        self.assertEqual(prepared_data, {
            'text': section_paragraph.paragraph,
            'title': section.title,
            'part': part.part_number,
            'date': version.effective_date,
            'section_order': section.sortable_label,
            'section_label': section.label,
            'short_name': part.short_name,
            'paragraph_id': section_paragraph.paragraph_id
        })

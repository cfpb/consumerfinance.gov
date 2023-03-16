from django.test import TestCase

from wagtail.documents.models import Document
from wagtail.models import Site

from search.elasticsearch_helpers import strip_html
from teachers_digital_platform.documents import ActivityPageDocument
from teachers_digital_platform.models import (
    ActivityIndexPage,
    ActivityPage,
    ActivityPageActivityDocuments,
    ActivityPageHandoutDocuments,
)


class TeachersDigitalPlatformDocumentTest(TestCase):
    fixtures = ["tdp_initial_data"]

    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.root_page = self.site.root_page
        self.activity_index_page = ActivityIndexPage(
            title="Search for activities",
            slug="activities",
        )
        docs = list(Document.objects.get(id=x) for x in range(8335, 8341))
        self.root_page.add_child(instance=self.activity_index_page)

        self.activity_page = ActivityPage(
            title="Storing my savings",
            slug="storing-my-savings",
            date="2020-02-21",
            live=True,
            summary="Students discuss safe places to store their money",
            big_idea="<p>You need a secure place to store your money.</p>",
            objectives=(
                "<ul><li>Understand different options to store your savings"
                "</li><li>Compare and contrast different options "
                "to store savings</li></ul>"
            ),
            essential_questions=(
                "</p><ul><li>What are some benefits and risks?</li>"
                "<li>What options for storing your savings works for you now?"
                "</li></ul><p></p>"
            ),
            what_students_will_do=(
                "<ul><li>Use the <strong>Evaluating savings scenarios</strong>"
                "worksheet to review real-world savingssituations.</li>"
                "<li>Recommend a savings tool(s) for each scenario.</li></ul>"
            ),
            activity_file=docs[0],
            handout_file=docs[1],
            handout_file_2=docs[2],
            handout_file_3=docs[3],
            activity_documents=[
                ActivityPageActivityDocuments(documents=docs[4])
            ],
            handout_documents=[
                ActivityPageHandoutDocuments(documents=docs[5]),
            ],
            activity_duration_id=1,
        )
        self.activity_index_page.add_child(instance=self.activity_page)
        self.activity_page.building_block = [1, 2, 3]
        self.activity_page.school_subject = [1]
        self.activity_page.topic = [1]
        self.activity_page.grade_level = [1]
        self.activity_page.age_range = [1]
        self.activity_page.student_characteristics = [1]
        self.activity_page.teaching_strategy = [1]
        self.activity_page.blooms_taxonomy_level = [1]
        self.activity_page.jump_start_coalition = [1]
        self.activity_page.council_for_economic_education = [1]
        # Re-add attached docs directly to object
        self.activity_page.activity_file = docs[0]
        self.activity_page.handout_file = docs[1]
        self.activity_page.handout_file_2 = docs[2]
        self.activity_page.handout_file_3 = docs[3]
        self.activity_page.save()

        self.doc = ActivityPageDocument()
        self.text_fields = [
            "big_idea",
            "essential_questions",
            "objectives",
            "related_text",
            "file_titles",
            "text",
            "title",
            "what_students_will_do",
            "id",
        ]
        self.date_fields = ["date"]
        self.keyword_fields = [
            "activity_duration",
            "activity_type",
            "age_range",
            "blooms_taxonomy_level",
            "building_block",
            "council_for_economic_education",
            "grade_level",
            "jump_start_coalition",
            "school_subject",
            "student_characteristics",
            "teaching_strategy",
            "topic",
        ]
        self.doc = ActivityPageDocument()

    def test_prepare(self):
        prepared_data = self.doc.prepare(self.activity_page)
        self.assertEqual(prepared_data.get("text"), self.activity_page.summary)
        for field in ["title", "date"]:
            self.assertEqual(
                prepared_data.get(field), getattr(self.activity_page, field)
            )
        self.assertEqual(
            prepared_data.get("big_idea"),
            strip_html(self.activity_page.big_idea),
        )
        prepared_file_titles = prepared_data.get("file_titles")
        for field in [
            "activity_file",
            "handout_file",
            "handout_file_2",
            "handout_file_3",
        ]:
            self.assertIn(
                getattr(self.activity_page, field).title,
                prepared_file_titles,
            )
        for field in ["activity_documents", "handout_documents"]:
            for link in getattr(self.activity_page, field).all():
                self.assertIn(
                    link.documents.title,
                    prepared_file_titles,
                )

    def test_model_class(self):
        self.assertEqual(self.doc.django.model, ActivityPage)

    def test_get_queryset(self):
        qs = ActivityPageDocument().get_queryset()
        self.assertEqual(
            qs.count(), ActivityPage.objects.filter(live=True).count()
        )

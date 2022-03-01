from django.test import TestCase

from wagtail.documents.models import Document

from model_bakery import baker

from teachers_digital_platform.models import (
    ActivityAgeRange,
    ActivityBloomsTaxonomyLevel,
    ActivityBuildingBlock,
    ActivityCouncilForEconEd,
    ActivityDuration,
    ActivityGradeLevel,
    ActivityIndexPage,
    ActivityJumpStartCoalition,
    ActivityPage,
    ActivitySchoolSubject,
    ActivityTeachingStrategy,
    ActivityTopic,
    ActivityType,
)
from v1.models import HomePage
from v1.tests.wagtail_pages.helpers import publish_page, save_new_page


class TestActivityPage(TestCase):
    fixtures = ["tdp_initial_data"]

    def setUp(self):
        super().setUp()
        self.ROOT_PAGE = HomePage.objects.get(slug="cfgov")
        self.ROOT_PAGE.save_revision().publish()

        self.index_page = ActivityIndexPage(
            live=True,
            depth=1,
            title="Test Index",
            slug="test-index",
            path="test-index",
        )
        publish_page(self.index_page)

    def test_get_subtopic_ids_returns_correct_subtopics(self):
        # Arrange
        activity_page = self.create_activity_detail_page("Test", "test")
        # Act
        actual_subtopic_ids = activity_page.get_subtopic_ids()
        # Assert
        self.assertNotIn(6, actual_subtopic_ids)
        self.assertIn(7, actual_subtopic_ids)

    def test_get_subtopic_ids_works_with_no_topics(self):
        # Arrange
        activity_page = self.create_activity_detail_page(
            "Test", "test", topic_list=[]
        )
        # Act
        actual_subtopic_ids = activity_page.get_subtopic_ids()
        # Assert
        self.assertIsInstance(actual_subtopic_ids, set)
        self.assertFalse(actual_subtopic_ids)

    def test_get_subtopic_ids_works_with_no_subtopics(self):
        # Arrange
        activity_page = self.create_activity_detail_page(
            "Test", "test", topic_list=[6]
        )
        # Act
        actual_subtopic_ids = activity_page.get_subtopic_ids()
        # Assert
        self.assertIsInstance(actual_subtopic_ids, set)
        self.assertFalse(actual_subtopic_ids)

    def test_get_grade_level_ids_returns_correct_grade_levels(self):
        # Arrange
        activity_page = self.create_activity_detail_page("Test", "test")
        # Act
        actual_grade_level_ids = activity_page.get_grade_level_ids()
        # Assert
        self.assertIn(2, actual_grade_level_ids)
        self.assertEqual(len(actual_grade_level_ids), 1)

    def test_get_grade_level_ids_works_with_no_grade_levels(self):
        # Arrange
        activity_page = self.create_activity_detail_page(
            "Test", "test", grade_level_list=[]
        )
        # Act
        actual_grade_level_ids = activity_page.get_grade_level_ids()
        # Assert
        self.assertIsInstance(actual_grade_level_ids, list)
        self.assertFalse(actual_grade_level_ids)

    def test_get_related_activities_url(self):
        # Arrange
        activity_page = self.create_activity_detail_page(
            "Test",
            "test",
        )
        save_new_page(activity_page, self.index_page)
        # Act
        actual_url = activity_page.get_related_activities_url()
        # Assert
        self.assertEqual(actual_url, "/test-index/?q=&topic=7&grade_level=2")

    def test_get_related_activities_url_with_multiple_grade_levels(self):
        # Arrange
        activity_page = self.create_activity_detail_page(
            "Test 2", "test-2", grade_level_list=[1, 2]
        )
        save_new_page(activity_page, self.index_page)
        # Act
        actual_url = activity_page.get_related_activities_url()
        # Assert
        self.assertEqual(
            actual_url, "/test-index/?q=&topic=7&grade_level=1&grade_level=2"
        )

    def test_get_related_activities_url_with_no_topics(self):
        # Arrange
        activity_page = self.create_activity_detail_page(
            "Test 2", "test-2", topic_list=[]
        )
        save_new_page(activity_page, self.index_page)
        # Act
        actual_url = activity_page.get_related_activities_url()
        # Assert
        self.assertEqual(actual_url, "/test-index/?q=&grade_level=2")

    def create_activity_detail_page(
        self,
        title="title",
        slug="slug",
        topic_list=[6, 7],
        grade_level_list=[2],
    ):  # noqa: B950
        activity_page = ActivityPage(
            live=True,
            title=title,
            slug=slug,
            path=slug,
            activity_file=baker.make(Document),
            date="2018-07-31",
            summary="Students will discuss short-term and long-term goals and what\r\nmakes a goal SMART. They\u2019ll then create a short-term savings goal\r\nand make a plan to meet that goal.",  # noqa: B950
            big_idea="<p>Saving money is essential to a positive\u00a0financial future.</p>",  # noqa: B950
            objectives="<ul><li>Understand the importance of setting SMARTsavings goals<br/></li><li>Create a short-term SMART savings goal</li><li>Make an action plan to save money</li></ul>",  # noqa: B950
            essential_questions="<p></p><ul><li>How can I reach my savings goals?<br/></li></ul><p></p>",  # noqa: B950
            what_students_will_do="<ul><li>Use the \u201cCreating a savings plan\u201d worksheet to\u00a0brainstorm a financial goal<br/></li><li>Create a SMART goal and a savings plan to\u00a0achieve this goal</li></ul>",  # noqa: B950
            building_block=ActivityBuildingBlock.objects.filter(
                pk__in=[2]
            ).all(),  # noqa: B950
            school_subject=ActivitySchoolSubject.objects.filter(
                pk__in=[1, 4]
            ).all(),  # noqa: B950
            topic=ActivityTopic.objects.filter(pk__in=topic_list).all(),
            grade_level=ActivityGradeLevel.objects.filter(
                pk__in=grade_level_list
            ).all(),  # noqa: B950
            age_range=ActivityAgeRange.objects.filter(pk__in=[2]).all(),
            student_characteristics=[],
            activity_type=ActivityType.objects.filter(pk__in=[1, 2, 3]).all(),
            teaching_strategy=ActivityTeachingStrategy.objects.filter(
                pk__in=[6, 7]
            ).all(),  # noqa: B950
            blooms_taxonomy_level=ActivityBloomsTaxonomyLevel.objects.filter(
                pk__in=[6]
            ).all(),  # noqa: B950
            activity_duration=ActivityDuration.objects.get(pk=2),
            council_for_economic_education=ActivityCouncilForEconEd.objects.filter(
                pk__in=[4]
            ).all(),  # noqa: B950
            jump_start_coalition=ActivityJumpStartCoalition.objects.filter(
                pk__in=[1]
            ).all(),  # noqa: B950
        )
        return activity_page

from django.test import RequestFactory, TestCase

from wagtail.core.blocks import StreamValue
from wagtail.core.models import Site
from wagtail.documents.models import Document
from wagtail.tests.utils import WagtailPageTests

import mock
from model_bakery import baker

from scripts import _atomic_helpers as atomic
from teachers_digital_platform.models import (
    ActivityAgeRange, ActivityBloomsTaxonomyLevel, ActivityBuildingBlock,
    ActivityCouncilForEconEd, ActivityDuration, ActivityGradeLevel,
    ActivityIndexPage, ActivityJumpStartCoalition, ActivityPage,
    ActivitySchoolSubject, ActivityStudentCharacteristics,
    ActivityTeachingStrategy, ActivityTopic, ActivityType
)
from v1.models import HomePage
from v1.tests.wagtail_pages.helpers import publish_page


class ActivityIndexPageTests(WagtailPageTests):
    @classmethod
    def setUpClass(self):
        super(ActivityIndexPageTests, self).setUpClass()

    def test_can_create_an_activity_page_under_activity_index_page(self):
        self.assertCanCreateAt(ActivityIndexPage, ActivityPage)

    def test_can_not_create_an_activity_index_page_under_activity_page(self):
        self.assertCanNotCreateAt(ActivityPage, ActivityIndexPage)

    def test_can_not_create_an_activity_page_under_home_page(self):
        self.assertCanNotCreateAt(ActivityPage, HomePage)

    def test_activity_page_parent_pages(self):
        self.assertAllowedParentPageTypes(
            ActivityPage,
            {ActivityIndexPage, HomePage}
        )

    def test_can_create_activity_index_page(self):
        ROOT_PAGE = HomePage.objects.first()
        self.assertCanCreate(
            ROOT_PAGE,
            ActivityIndexPage,
            {
                'title': 'Search for activities',
                'header-count': '0',
                'header_sidebar-count': '0',
                'sidefoot-count': '0',
                'categories-TOTAL_FORMS': '0',
                'categories-INITIAL_FORMS': '0',
                'categories-MIN_NUM_FORMS': '0',
                'categories-MAX_NUM_FORMS': '2',
                'language': 'en',
                'is_archived': 'no',
            }
        )


class TestActivityIndexPageSearch(TestCase):
    fixtures = ['tdp_initial_data']

    def setUp(self):
        super(TestActivityIndexPageSearch, self).setUp()
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.ROOT_PAGE.save_revision().publish()
        self.site = Site.objects.get(is_default_site=True)
        self.factory = RequestFactory()
        self.search_page = ActivityIndexPage(
            live=True,
            path='search',
            depth='1',
            title='Search for activities',
            slug='search'
        )
        self.search_page.header = StreamValue(self.search_page.header.stream_block, [atomic.text_introduction], True)  # noqa: E501
        publish_page(child=self.search_page)

    def get_request(self, path='', data={}):
        request = self.factory.get(path, data=data)
        return request

    def test_activity_index_page_renders(self):
        # Arrange
        response = self.search_page.make_preview_request()
        # Act
        response.render()
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_activity_index_page_renders_with_query_parameters(self):
        # Arrange
        response = self.search_page.make_preview_request()
        # Act
        response.render()
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_search_page_get_template(self):
        # Act
        search_reqeust = self.get_request()
        # Assert
        self.assertEqual(
            self.search_page.get_template(search_reqeust),
            'teachers_digital_platform/activity_index_page.html')

    def test_search_results_page_get_template(self):
        # Arrange
        request = self.get_request(data={'partial': 'true'})
        self.assertEqual(
            self.search_page.get_template(request),
            'teachers_digital_platform/activity_search_facets_and_results.html')  # noqa: E501
        # Act - Should return partial results even if no value is provided
        request = self.get_request(data={'partial': ''})
        # Assert
        self.assertEqual(
            self.search_page.get_template(request),
            'teachers_digital_platform/activity_search_facets_and_results.html')  # noqa: E501

    def test_search_index_page_handles_bad_query(self):
        # Arrange
        response = self.search_page.make_preview_request()
        # Act
        response.render()
        # Assert
        self.assertTrue(b'<h3>No results match your search.</h3>' in response.content)  # noqa: E501

    @mock.patch('teachers_digital_platform.models.pages.SearchQuerySet.models')
    def test_search_get_all_facets_with_building_block_filter(self, mock_sqs):
        # Arrange
        facet_counts = {
            'dates': {},
            'fields': {
                'topic': ['1', '4'],
                'building_block': ['1', '2'],
                'school_subject': ['1'],
            },
            'queries': {}
        }
        selected_facets = {u'building_block': [1]}
        facet_queries = {'building_block': 'building_block_exact'}
        facet_map = self.create_facet_map()
        mock_sqs.facet_counts.return_value = facet_counts
        # Act
        actual_all_facets = self.search_page.get_all_facets(facet_map, mock_sqs, facet_counts, facet_queries, selected_facets)  # noqa: E501
        # Assert
        self.assertTrue('building_block' in actual_all_facets)

    @mock.patch('teachers_digital_platform.models.pages.SearchQuerySet.models')
    def test_search_get_all_facets_with_topic_block_is_nested_filter(self, mock_sqs):  # noqa: E501
        # Arrange
        facet_counts = {
            'dates': {},
            'fields': {
                'topic': ['4'],
            },
            'queries': {}
        }
        selected_facets = {u'topic': [1]}
        facet_queries = {'topic': 'topic_exact'}
        facet_map = self.create_facet_map()
        mock_sqs.facet_counts.return_value = facet_counts
        # Act
        actual_all_facets = self.search_page.get_all_facets(facet_map, mock_sqs, facet_counts, facet_queries, selected_facets)  # noqa: E501
        # Assert
        self.assertTrue('topic' in actual_all_facets)

    def test_get_topics_list_returns_correct_topic_list_for_parent(self):
        # Arrange
        activity_page = self.create_activity_detail_page(title='Planning for future savings', slug='planning-future-savings')  # noqa: E501
        # Act
        actual_topics_list = activity_page.get_topics_list(self.search_page)
        # Assert
        self.assertTrue('activities' in actual_topics_list)

    def test_get_topics_list_returns_correct_topic_list_no_parent(self):
        # Arrange
        activity_page = self.create_activity_detail_page(title='Planning for future savings', slug='planning-future-savings')  # noqa: E501
        # Act
        actual_topics_list = activity_page.get_topics_list(None)
        # Assert
        self.assertTrue('Save and Invest (Saving for short-term goals)' in actual_topics_list)  # noqa: E501

    def create_facet_map(self):
        return (
            ('building_block', (ActivityBuildingBlock, False, 10)),
            ('school_subject', (ActivitySchoolSubject, False, 25)),
            ('topic', (ActivityTopic, True, 25)),
            ('grade_level', (ActivityGradeLevel, False, 10)),                           # noqa: E501
            ('age_range', (ActivityAgeRange, False, 10)),
            ('student_characteristics', (ActivityStudentCharacteristics, False, 10)),   # noqa: E501
            ('activity_type', (ActivityType, False, 10)),
            ('teaching_strategy', (ActivityTeachingStrategy, False, 25)),               # noqa: E501
            ('blooms_taxonomy_level', (ActivityBloomsTaxonomyLevel, False, 25)),        # noqa: E501
            ('activity_duration', (ActivityDuration, False, 10)),                       # noqa: E501
            ('jump_start_coalition', (ActivityJumpStartCoalition, False, 25)),          # noqa: E501
            ('council_for_economic_education', (ActivityCouncilForEconEd, False, 25)),  # noqa: E501
        )

    def create_activity_detail_page(self, title='title', slug='slug'):
        activity_page = ActivityPage(
            live=True,
            title=title,
            slug=slug,
            path=slug,
            activity_file=baker.make(Document),
            date="2018-07-31",
            summary="Students will discuss short-term and long-term goals and what\r\nmakes a goal SMART. They\u2019ll then create a short-term savings goal\r\nand make a plan to meet that goal.",  # noqa: E501
            big_idea="<p>Saving money is essential to a positive\u00a0financial future.</p>",           # noqa: E501
            objectives="<ul><li>Understand the importance of setting SMARTsavings goals<br/></li><li>Create a short-term SMART savings goal</li><li>Make an action plan to save money</li></ul>",  # noqa: E501
            essential_questions="<p></p><ul><li>How can I reach my savings goals?<br/></li></ul><p></p>",  # noqa: E501
            what_students_will_do="<ul><li>Use the \u201cCreating a savings plan\u201d worksheet to\u00a0brainstorm a financial goal<br/></li><li>Create a SMART goal and a savings plan to\u00a0achieve this goal</li></ul>",  # noqa: E501
            building_block=ActivityBuildingBlock.objects.filter(pk__in=[2]).all(),                      # noqa: E501
            school_subject=ActivitySchoolSubject.objects.filter(pk__in=[1, 4]).all(),                   # noqa: E501
            topic=ActivityTopic.objects.filter(pk__in=[6, 11]).all(),
            grade_level=ActivityGradeLevel.objects.filter(pk__in=[2]).all(),
            age_range=ActivityAgeRange.objects.filter(pk__in=[2]).all(),
            student_characteristics=[],
            activity_type=ActivityType.objects.filter(pk__in=[1, 2, 3]).all(),
            teaching_strategy=ActivityTeachingStrategy.objects.filter(pk__in=[6, 7]).all(),             # noqa: E501
            blooms_taxonomy_level=ActivityBloomsTaxonomyLevel.objects.filter(pk__in=[6]).all(),         # noqa: E501
            activity_duration=ActivityDuration.objects.get(pk=2),
            council_for_economic_education=ActivityCouncilForEconEd.objects.filter(pk__in=[4]).all(),   # noqa: E501
            jump_start_coalition=ActivityJumpStartCoalition.objects.filter(pk__in=[1]).all()            # noqa: E501
        )
        return activity_page


# print_to_file(response.content, 'response.html')
def print_to_file(text, filename):
    handle1 = open(filename, 'w+')
    handle1.write(text)
    handle1.close()

from django.test import RequestFactory, TestCase, override_settings

from wagtail.core.blocks import StreamValue
from wagtail.core.models import Site
from wagtail.documents.models import Document
from wagtail.tests.utils import WagtailPageTests

import mock
from model_bakery import baker

from scripts import _atomic_helpers as atomic
from teachers_digital_platform.models import (
    FACET_LIST, FACET_MAP, ActivityAgeRange, ActivityBloomsTaxonomyLevel,
    ActivityBuildingBlock, ActivityCouncilForEconEd, ActivityDuration,
    ActivityGradeLevel, ActivityIndexPage, ActivityJumpStartCoalition,
    ActivityPage, ActivitySchoolSubject, ActivitySetUp,
    ActivityTeachingStrategy, ActivityTopic, ActivityType, get_activity_setup
)
from v1.models import HomePage


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
        root_page = HomePage.objects.first()
        self.assertCanCreate(
            root_page,
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


class ActivitySetUpTests(TestCase):

    fixtures = ['tdp_initial_data']

    def setUp(self):
        self.doc = baker.make(Document, pk=1)
        self.home_page = HomePage.objects.first()
        self.search_page = ActivityIndexPage(
            live=True,
            title='Search for activities',
            slug='search',
        )
        self.home_page.add_child(instance=self.search_page)
        self.activity_page = ActivityPage(
            title="Test Activity Page",
            slug='test-activity-page',
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
            activity_file_id=1,
            activity_duration_id=1,
        )
        self.home_page.add_child(instance=self.activity_page)
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
        self.activity_page.save()

    def test_facet_setup_creation(self):
        # get_activity_setup creates a setup object
        self.assertEqual(ActivitySetUp.objects.count(), 0)
        get_activity_setup()
        self.assertEqual(ActivitySetUp.objects.count(), 1)
        setup_obj = ActivitySetUp.objects.first()
        # number of cards should match number of live activity pages
        self.assertEqual(
            len(setup_obj.card_setup),
            ActivityPage.objects.filter(live=True).count()
        )
        # number of facets should match length of master facet list
        self.assertEqual(
            len(setup_obj.facet_setup),
            len(FACET_LIST)
        )

    def test_taxonomy_model_str(self):
        taxonomy_instance = ActivityBuildingBlock.objects.first()
        self.assertEqual(
            str(taxonomy_instance),
            taxonomy_instance.title
        )

    def test_mptt_model_str(self):
        mptt_instance = ActivityTopic.objects.first()
        self.assertEqual(
            str(mptt_instance),
            mptt_instance.title
        )


class TestActivityIndexPageSearch(TestCase):
    fixtures = ['tdp_initial_data']

    def setUp(self):
        # super(TestActivityIndexPageSearch, self).setUp()
        self.root_page = HomePage.objects.get(slug='cfgov')
        self.root_page.save_revision().publish()
        self.site = Site.objects.get(is_default_site=True)
        self.factory = RequestFactory()
        self.search_page = ActivityIndexPage(
            title='Search for activities',
            slug='activities_search'
        )
        self.search_page.header = StreamValue(
            self.search_page.header.stream_block,
            [atomic.text_introduction],
            True
        )
        self.root_page.add_child(instance=self.search_page)
        self.root_page.save_revision().publish()
        self.activity_setups = get_activity_setup()

    def get_request(self, path='', data={}):
        request = self.factory.get(path, data=data)
        return request

    @mock.patch(
        'teachers_digital_platform.models.activity_index_page.'
        'ActivityIndexPage.haystack_search')
    def test_activity_index_page_renders_via_haystack(self, mock_haystack):
        mock_haystack.return_value = {
            "facets": self.activity_setups.facet_setup,
        }
        response = self.client.get(self.search_page.url)
        self.assertEqual(response.status_code, 200)

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_TDP": [("boolean", True)]})
    @mock.patch(
        'teachers_digital_platform.models.activity_index_page.'
        'ActivityIndexPage.dsl_search')
    def test_activity_index_page_renders_via_dsl(self, mock_dsl):
        mock_dsl.return_value = {
            "facets": self.activity_setups.facet_setup,
        }
        response = self.client.get(self.search_page.url)
        self.assertEqual(response.status_code, 200)

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_TDP": [("boolean", True)]})
    @mock.patch(
        'teachers_digital_platform.models.activity_index_page.'
        'ActivityIndexPage.dsl_search')
    def test_activity_index_page_renders_with_query_parameters(self, mock_dsl):
        mock_dsl.return_value = {
            "facets": self.activity_setups.facet_setup,
        }
        self.search_page.results = {
            self.activity_setups.card_setup.values()
        }
        response = self.client.get(f"{self.search_page.url}?q=test-query")
        self.assertEqual(response.status_code, 200)

    def test_search_page_get_template(self):
        search_request = self.get_request()
        self.assertEqual(
            self.search_page.get_template(search_request),
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

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_TDP": [("boolean", True)]})
    @mock.patch(
        'teachers_digital_platform.models.activity_index_page.'
        'ActivityIndexPage.dsl_search')
    def test_search_index_page_handles_empty_query(self, mock_search):
        mock_search.return_value = {
            "facets": self.activity_setups.facet_setup,
        }
        response = self.client.get(f"{self.search_page.url}?q=")
        self.assertIn(
            '<h3>No results match your search.</h3>',
            response.content.decode('utf8'))

    @mock.patch(
        'teachers_digital_platform.models.'
        'activity_index_page.SearchQuerySet.models')
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
        facet_map = FACET_MAP
        mock_sqs.facet_counts.return_value = facet_counts
        # Act
        actual_all_facets = self.search_page.get_all_facets(facet_map, mock_sqs, facet_counts, facet_queries, selected_facets)  # noqa: E501
        # Assert
        self.assertTrue('building_block' in actual_all_facets)

    @mock.patch(
        'teachers_digital_platform.models.'
        'activity_index_page.SearchQuerySet.models')
    def test_search_get_all_facets_with_topic_block_is_nested_filter(
            self, mock_sqs):
        # Arrange
        facet_counts = {
            'dates': {},
            'fields': {
                'topic': ['4'],
            },
            'queries': {}
        }
        selected_facets = {'topic': [1]}
        facet_queries = {'topic': 'topic_exact'}
        facet_map = FACET_MAP
        mock_sqs.facet_counts.return_value = facet_counts
        # Act
        actual_all_facets = self.search_page.get_all_facets(
            facet_map, mock_sqs, facet_counts, facet_queries, selected_facets)
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
# def print_to_file(text, filename):
#     with open(filename, 'w+') as f:
#         f.write(text)

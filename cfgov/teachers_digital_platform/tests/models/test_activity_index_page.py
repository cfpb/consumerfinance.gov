from collections import OrderedDict
from unittest import mock

from django.http import HttpRequest
from django.test import RequestFactory, TestCase

from wagtail.core.blocks import StreamValue
from wagtail.core.models import Site
from wagtail.documents.models import Document
from wagtail.tests.utils import WagtailPageTests

from model_bakery import baker

from scripts import _atomic_helpers as atomic
from teachers_digital_platform.models import (
    FACET_LIST,
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
    ActivitySetUp,
    ActivityTeachingStrategy,
    ActivityTopic,
    ActivityType,
    get_activity_setup,
)
from teachers_digital_platform.models.activity_index_page import (
    Paginator,
    parse_dsl_facets,
    validate_page_number,
)
from v1.models import HomePage


class ActivityIndexPageTests(WagtailPageTests):
    @classmethod
    def setUpClass(self):
        super().setUpClass()

    def test_can_create_an_activity_page_under_activity_index_page(self):
        self.assertCanCreateAt(ActivityIndexPage, ActivityPage)

    def test_can_not_create_an_activity_index_page_under_activity_page(self):
        self.assertCanNotCreateAt(ActivityPage, ActivityIndexPage)

    def test_can_not_create_an_activity_page_under_home_page(self):
        self.assertCanNotCreateAt(ActivityPage, HomePage)

    def test_activity_page_parent_pages(self):
        self.assertAllowedParentPageTypes(
            ActivityPage, {ActivityIndexPage, HomePage}
        )

    def test_can_create_activity_index_page(self):
        root_page = HomePage.objects.first()
        self.assertCanCreate(
            root_page,
            ActivityIndexPage,
            {
                "title": "Search for activities",
                "header-count": "0",
                "header_sidebar-count": "0",
                "sidefoot-count": "0",
                "categories-TOTAL_FORMS": "0",
                "categories-INITIAL_FORMS": "0",
                "categories-MIN_NUM_FORMS": "0",
                "categories-MAX_NUM_FORMS": "2",
                "language": "en",
                "is_archived": "no",
            },
        )


class ActivitySetUpTests(TestCase):

    from teachers_digital_platform.documents import ActivityPageDocument

    fixtures = ["tdp_initial_data"]

    def setUp(self):
        self.doc = baker.make(Document, pk=1)
        self.home_page = HomePage.objects.get(slug="cfgov")
        self.home_page.save_revision().publish()
        self.search_page = ActivityIndexPage(
            live=True,
            title="Search for activities",
            slug="activity-search",
        )
        self.search_page.header = StreamValue(
            self.search_page.header.stream_block,
            [atomic.text_introduction],
            True,
        )
        self.home_page.add_child(instance=self.search_page)
        self.activity_page = ActivityPage(
            title="Test Activity Page",
            slug="test-activity-page",
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
        self.search_page.add_child(instance=self.activity_page)
        self.activity_page.building_block = [1, 2, 3]
        self.activity_page.school_subject = [1]
        self.activity_page.topic = [1, 2, 3, 14]
        self.activity_page.grade_level = [1]
        self.activity_page.age_range = [1]
        self.activity_page.student_characteristics = [1]
        self.activity_page.teaching_strategy = [1]
        self.activity_page.blooms_taxonomy_level = [1]
        self.activity_page.jump_start_coalition = [1]
        self.activity_page.council_for_economic_education = [1]
        self.activity_page.activity_setups = get_activity_setup()
        self.activity_page.save()

    def test_setup_str(self):
        self.assertEqual(
            ActivitySetUp().__str__(), "Cached activity facets and cards"
        )

    def test_facet_setup_creation(self):
        """get_activity_setup should ensure existence of a setup object."""
        live_count = ActivityPage.objects.filter(live=True).count()
        get_activity_setup()
        self.assertTrue(ActivitySetUp.objects.exists())
        setup_obj = ActivitySetUp.objects.first()
        # number of cards should match number of live activity pages
        self.assertEqual(len(setup_obj.card_setup), live_count)
        # ordered_cards should be an ordered dict of all live activities
        self.assertTrue(isinstance(setup_obj.ordered_cards, OrderedDict))
        self.assertEqual(len(setup_obj.ordered_cards), live_count)
        # number of facets should match length of master facet list
        self.assertEqual(len(setup_obj.facet_setup), len(FACET_LIST))
        page1 = ActivityPage.objects.filter(live=True).first()
        page1.summary = "Changed summary" + page1.summary
        page1.save()
        new_setup_obj = get_activity_setup(refresh=True)
        self.assertNotEqual(setup_obj.card_setup, new_setup_obj.card_setup)

    def test_dsl_facet_parsing(self):
        all_facets = self.activity_page.activity_setups.facet_setup
        original_topic_count = len(all_facets["topic"])
        original_subject_count = len(all_facets["school_subject"])
        facet_response = {
            "building_block": [
                {"key": "1", "doc_count": 14},
                {"key": "2", "doc_count": 40},
                {"key": "3", "doc_count": 18},
            ],
            "school_subject": [{"key": "1", "doc_count": 24}],
            "topic": [
                {"key": "1", "doc_count": 6},
                {"key": "2", "doc_count": 6},
                {"key": "3", "doc_count": 6},
                {"key": "14", "doc_count": 6},
            ],
            "grade_level": [{"key": "1", "doc_count": 11}],
            "age_range": [{"key": "1", "doc_count": 11}],
            "student_characteristics": [{"key": "1", "doc_count": 26}],
            "activity_type": [{"key": "1", "doc_count": 26}],
            "teaching_strategy": [{"key": "1", "doc_count": 2}],
            "blooms_taxonomy_level": [{"key": "1", "doc_count": 4}],
            "activity_duration": [{"key": "1", "doc_count": 8}],
            "jump_start_coalition": [{"key": "1", "doc_count": 24}],
            "council_for_economic_education": [{"key": "1", "doc_count": 14}],
        }
        selected_facets = {"topic": ["1", "2", "14"], "school_subject": ["1"]}
        new_all_facets = parse_dsl_facets(
            all_facets, facet_response, selected_facets
        )
        new_topic_count = len(new_all_facets["topic"])
        new_subject_count = len(new_all_facets["school_subject"])
        self.assertNotEqual(original_topic_count, new_topic_count)
        self.assertNotEqual(original_subject_count, new_subject_count)

    def test_bare_dsl_search_uses_setups(self):
        """Search with no query or faceting should not need Elasticsearch."""
        response = self.client.get(self.search_page.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.activity_page.title, response.content.decode("utf8")
        )

    @mock.patch.object(ActivityPageDocument, "search")
    def test_search_page_renders_with_query_parameter(self, mock_search):
        mock_hit = mock.Mock()
        mock_hit.id = self.activity_page.pk
        mock_search().query().count.return_value = 1
        mock_search().query().__getitem__().execute.return_value = [mock_hit]
        response = self.client.get(f"{self.search_page.url}?q=test-query")
        self.assertEqual(response.status_code, 200)
        self.assertIn("test-query", response.content.decode("utf8"))

    @mock.patch.object(ActivityPageDocument, "search")
    def test_search_page_renders_with_facet_parameters(self, mock_search):
        mock_hit = mock.Mock()
        mock_hit.id = self.activity_page.pk
        mock_search().query().count.return_value = 1
        mock_search().query().__getitem__().execute.return_value = [mock_hit]
        mock_facet_response = mock.Mock()
        mock_facet_response.aggregations = mock.Mock()
        mock_facet_response.aggregations.buckets = mock.Mock(
            return_value=iter(
                {"topic": [{"key": "1"}, {"key": "2"}, {"key": "3"}]}
            )
        )
        mock_search().sort().query().count.return_value = 1
        mock_search().sort().query().__getitem__().execute.return_value = [
            mock_hit
        ]
        mock_search().sort().query().update_from_dict().__getitem__().execute.return_value = (  # noqa: B950
            mock_facet_response
        )
        response = self.client.get(
            f"{self.search_page.url}?topic=1&topic=2&topic=3"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("topic=1", response.content.decode("utf8"))

    def test_taxonomy_model_str(self):
        taxonomy_instance = ActivityBuildingBlock.objects.first()
        self.assertEqual(str(taxonomy_instance), taxonomy_instance.title)

    def test_mptt_model_str(self):
        mptt_instance = ActivityTopic.objects.first()
        self.assertEqual(str(mptt_instance), mptt_instance.title)

    def test_validate_pagination_number(self):
        paginator = Paginator([{"fake": "results"}] * 30, 25)
        request = HttpRequest()
        self.assertEqual(validate_page_number(request, paginator), 1)
        request.GET.update({"page": "2"})
        self.assertEqual(validate_page_number(request, paginator), 2)
        request = HttpRequest()
        request.GET.update({"page": "1000"})
        self.assertEqual(validate_page_number(request, paginator), 1)
        request = HttpRequest()
        request.GET.update({"page": "<script>Boo</script>"})
        self.assertEqual(validate_page_number(request, paginator), 1)


class TestActivityIndexPageSearch(TestCase):
    fixtures = ["tdp_initial_data"]

    def setUp(self):
        # super().setUp()
        self.root_page = HomePage.objects.get(slug="cfgov")
        self.root_page.save_revision().publish()
        self.site = Site.objects.get(is_default_site=True)
        self.factory = RequestFactory()
        self.search_page = ActivityIndexPage(
            title="Search for activities", slug="activities_search"
        )
        self.search_page.header = StreamValue(
            self.search_page.header.stream_block,
            [atomic.text_introduction],
            True,
        )
        self.root_page.add_child(instance=self.search_page)
        self.root_page.save_revision().publish()
        self.activity_setups = get_activity_setup()

    def get_request(self, path="", data=None):
        if not data:
            data = {}
        request = self.factory.get(path, data=data)
        return request

    @mock.patch(
        "teachers_digital_platform.models.activity_index_page."
        "ActivityIndexPage.dsl_search"
    )
    def test_search_page_renders_via_dsl_search(self, mock_dsl):
        mock_dsl.return_value = {
            "facets": self.activity_setups.facet_setup,
        }
        response = self.client.get(self.search_page.url)
        self.assertEqual(response.status_code, 200)

    def test_search_page_get_template(self):
        search_request = self.get_request()
        self.assertEqual(
            self.search_page.get_template(search_request),
            "teachers_digital_platform/activity_index_page.html",
        )

    def test_search_results_page_get_template(self):
        # Arrange
        request = self.get_request(data={"partial": "true"})
        self.assertEqual(
            self.search_page.get_template(request),
            "teachers_digital_platform/activity_search_facets_and_results.html",
        )  # noqa: B950
        # Act - Should return partial results even if no value is provided
        request = self.get_request(data={"partial": ""})
        # Assert
        self.assertEqual(
            self.search_page.get_template(request),
            "teachers_digital_platform/activity_search_facets_and_results.html",
        )  # noqa: B950

    @mock.patch(
        "teachers_digital_platform.models.activity_index_page."
        "ActivityIndexPage.dsl_search"
    )
    def test_search_index_page_handles_no_results_query(self, mock_search):
        mock_search.return_value = {
            "facets": self.activity_setups.facet_setup,
        }
        response = self.client.get(f"{self.search_page.url}?q=xxxxxxxxxx")
        self.assertIn(
            "<h3>No results match your search.</h3>",
            response.content.decode("utf8"),
        )

    def test_get_topics_list_returns_correct_topic_list_for_parent(self):
        # Arrange
        activity_page = self.create_activity_detail_page(
            title="Planning for future savings", slug="planning-future-savings"
        )  # noqa: B950
        # Act
        actual_topics_list = activity_page.get_topics_list(self.search_page)
        # Assert
        self.assertTrue("activities" in actual_topics_list)

    def test_get_topics_list_returns_correct_topic_list_no_parent(self):
        # Arrange
        activity_page = self.create_activity_detail_page(
            title="Planning for future savings", slug="planning-future-savings"
        )  # noqa: B950
        # Act
        actual_topics_list = activity_page.get_topics_list(None)
        # Assert
        self.assertTrue(
            "Save and Invest (Saving for short-term goals)"
            in actual_topics_list
        )  # noqa: B950

    def create_activity_detail_page(self, title="title", slug="slug"):
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
            topic=ActivityTopic.objects.filter(pk__in=[6, 11]).all(),
            grade_level=ActivityGradeLevel.objects.filter(pk__in=[2]).all(),
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


# print_to_file(response.content, 'response.html')
# def print_to_file(text, filename):
#     with open(filename, 'w+') as f:
#         f.write(text)

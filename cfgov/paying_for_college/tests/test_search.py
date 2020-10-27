import json

from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

import mock

from paying_for_college.documents import SchoolDocument
from paying_for_college.models import School
from paying_for_college.models.search import SchoolSearch
from paying_for_college.views import school_autocomplete, school_search_api


# paying-for-college2/understanding-your-financial-aid-offer/api/search-schools.json?q=Kansas
class SchoolSearchTest(TestCase):

    fixtures = ["test_fixture.json"]

    class ElasticSchool:
        def __init__(self):
            self.text = ""
            self.school_id = 0
            self.city = ""
            self.state = ""
            self.nicknames = ""
            self.zip5 = ""
            self.url = ""

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_PFC": [("boolean", True)]})
    @mock.patch.object(SchoolDocument, 'search')
    def test_school_autocomplete(self, mock_autocomplete):
        term = "Kansas"
        school = School.objects.get(pk=155317)
        school.save()
        # mock the search returned value
        mock_return = mock.Mock()
        mock_return.text = school.primary_alias
        mock_return.school_id = school.school_id
        mock_return.city = school.city
        mock_return.state = school.state
        mock_return.zip5 = school.zip5
        mock_return.nicknames = "Jayhawks"
        # mock_autocomplete.return_value = [mock_return]
        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_queryset.count.return_value = 1
        # mock_autocomplete.return_value = mock_queryset
        mock_autocomplete().query().filter().sort() \
            .__getitem__().execute.return_value = [mock_return]
        mock_count = mock.Mock(return_value=1)
        mock_autocomplete().query().count = mock_count
        mock_autocomplete().query().filter().sort() \
            .__getitem__().count = mock_count
        url = "{}?q=Kansas".format(
            reverse("paying_for_college:disclosures:school_search")
        )
        response = school_autocomplete(RequestFactory().get(url))
        # output = json.loads(response.content)
        # self.assertEqual(sorted(output[0].keys()), ["id", "schoolname"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_autocomplete.call_count, 4)
        self.assertTrue(mock_autocomplete.called_with(search_term=term))
        self.assertTrue("Kansas" in mock_return.text)
        self.assertEqual(155317, mock_return.school_id)
        self.assertTrue("Jayhawks" in mock_return.nicknames)
        self.assertTrue("Lawrence" in mock_return.city)
        self.assertTrue("KS" in mock_return.state)

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_PFC": [("boolean", True)]})
    @mock.patch.object(SchoolDocument, 'search')
    def test_autocomplete_no_term(self, mock_search):
        term = ""
        mock_return = mock.Mock()
        mock_return.search_term = term
        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_queryset.count.return_value = 1
        response = self.client.get(
            reverse("paying_for_college:disclosures:school_search"),
            {"q": term}
        )
        self.assertEqual(mock_search.call_count, 0)
        self.assertEqual(response.status_code, 200)

    @override_settings(FLAGS={"ELASTICSEARCH_DSL_PFC": [("boolean", True)]})
    @mock.patch.object(SchoolSearch, 'autocomplete')
    def test_autocomplete_blank_term(self, mock_autocomplete):
        url = "{}?q=".format(
            reverse("paying_for_college:disclosures:school_search")
        )
        response = school_autocomplete(RequestFactory().get(url))
        self.assertEqual(json.loads(response.content), [])
        self.assertEqual(mock_autocomplete.call_count, 0)
        self.assertEqual(response.status_code, 200)

    # TODO: delete the test_school_search_api function after we migrate to ES7
    @mock.patch("paying_for_college.views.SearchQuerySet.autocomplete")
    def test_school_search_api(self, mock_autocomplete):
        """school_search_api should return json."""

        school = School.objects.get(pk=155317)
        # mock the search returned value
        elastic_school = self.ElasticSchool()
        elastic_school.text = school.primary_alias
        elastic_school.school_id = school.school_id
        elastic_school.city = school.city
        elastic_school.state = school.state
        elastic_school.nicknames = "Jayhawks"
        mock_autocomplete.return_value = [elastic_school]
        url = "{}?q=Kansas".format(
            reverse("paying_for_college:disclosures:school_search")
        )
        response = school_search_api(RequestFactory().get(url))
        self.assertTrue(b"Kansas" in response.content)
        self.assertTrue(b"155317" in response.content)
        self.assertTrue(b"Jayhawks" in response.content)

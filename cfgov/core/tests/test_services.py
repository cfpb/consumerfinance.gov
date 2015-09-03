import mock
import icalendar
from django.test import TestCase

from core.services import ICSView


class ICSViewTest(TestCase):

    def setUp(self):
        pass

    @mock.patch('requests.get')
    def test_get_event_json(self, mock_request_get):
        """
        Test that we're constructing the event source URL from which to fetch
        JSON correctly.
        """
        # We want two possible responses, first a good, 200 response, and
        # then a 404 response (a response that doesn't provide JSON). We
        # need to make sure we're handling the ValueError (JSONDecodeError).
        mock_good_response = mock.MagicMock()
        mock_good_response.status_code = 200
        mock_good_response.json.return_value = {'ics': {'some': 'json'}}

        mock_bad_response = mock.MagicMock()
        mock_bad_response.status_code = 404
        mock_bad_response.json.side_effect = ValueError()

        mock_request_get.side_effect = [
            mock_good_response,
            mock_bad_response
        ]
        view = ICSView(
            event_source='http://localhost:9200/events/<event_slug>/')

        source_status = view.get_event_json('myevent')
        self.assertEqual(source_status, 200)
        mock_request_get.assert_called_with(
            'http://localhost:9200/events/myevent/')

        source_status = view.get_event_json('myevent')
        self.assertEqual(source_status, 404)
        self.assertEqual(view.event_json, {})

    def test_generate_ics(self):
        """
        Test that, given a specific set of JSON, the generate_ics
        function generates valid iCalendar data.
        """
        view = ICSView(
            event_source='http://localhost:9200/events/<event_slug>/')
        view.event_json = {
            'ics': {
                'summary': 'Test Event',
                'location': 'Washington, DC',
                'uid': '8DB71F484FA2ABC57F621CB7F1@2013-07-03 09:30:00',
                'dtstart': '2015-07-01T05:00:00-04:00',
                'starting_tzinfo': 'America/New_York',
                'dtend': '2015-07-01T06:00:00-04:00',
                'ending_tzinfo': 'America/New_York',
                'dtstamp': '2013-07-02T14:29:08'
            }
        }

        with mock.patch('core.services.ICSView.get_event_json') as \
                mock_get_event_json:
            mock_get_event_json.return_value = 200
            response = view.generate_ics('foo')

            # Make sure the ics parses
            try:
                icalendar.Calendar.from_ical(response.content)
            except ValueError:
                self.fail('generate_ics() did not return a valid iCalendar file')

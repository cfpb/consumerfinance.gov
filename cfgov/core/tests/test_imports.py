from django.test import TestCase
from django.conf import settings
from v1.processors import eventpage, contact
from core.management.commands import import_data
import collections

class ImportDataTest(TestCase):

    def test_eventpage_formattags(self):
        tags = [u'Consumer Advisory Board', u'Consumer Engagement', u'Mortgage Servicing', u'Older Americans']
        expected_output = u'"Consumer Advisory Board", "Consumer Engagement", "Mortgage Servicing", "Older Americans"'
        output = eventpage.DataConverter().format_tags(tags)
        self.assertEqual(output, expected_output)

    def test_eventpage_formatauthor(self):
        author = {u'first_name': u'Sarah', u'last_name': u'Simpson', u'name': u'Sarah Simpson', u'url': u'', u'slug': u'sarah-simpson', u'nickname': u'sarah.simpson', u'id': 353, u'description': u''}
        expected_output = u'"Sarah Simpson"'
        output = eventpage.DataConverter().format_author(author)
        self.assertEqual(output, expected_output)

    def test_eventpage_venue(self):
        venue = {u'name': u'Japanese American National Museum', u'address': {u'city': u'Los Angeles', u'state': u'CA', u'street': u'100 North Central Ave', u'zip_code': u'90012'}}
        output = eventpage.DataConverter().get_venue_dict(venue)
        expected_output = {'venue_state': u'CA', 'venue_city': u'Los Angeles', 'venue_street': u'100 North Central Ave', 'venue_name': u'Japanese American National Museum'}
        self.assertEqual(output, expected_output)

    def test_get_event_processor(self):
        processor = import_data.Command().get_processor('events', settings.SHEER_PROCESSORS)
        self.assertEqual(processor.__name__, 'processors.wordpress_event')

    def test_get_contact_processor(self):
        processor = import_data.Command().get_processor('contact', settings.SHEER_PROCESSORS)
        self.assertEqual(processor.__name__, 'processors.wordpress_contact')

    def test_contact_convert(self):
        imported_data = {u'attachments': [], u'relative_url': u'/contact/your-money-your-goals-toolkit/', u'excerpt': u'<p>Your Money, Your Goals is a toolkit for social service organizations and others to use when working with low- and moderate-income and underserved consumers. The Office of Financial Empowerment can help you get started using YMYG in your work.</p>\n', u'id': 37397, 'web': {'url': u'http://www.consumerfinance.gov/your-money-your-goals/'}, u'author': {u'first_name': u'James', u'last_name': u'Hupp', u'name': u'James Hupp', u'url': u'', u'slug': u'jhupp', u'nickname': u'jhupp', u'id': 4, u'description': u''}, u'content': u'<p>Your Money, Your Goals is a toolkit for social service organizations and others to use when working with low- and moderate-income and underserved consumers. The Office of Financial Empowerment can help you get started using YMYG in your work.</p>\n', u'comment_count': 0, u'categories': [], u'type': u'contact', 'email': [{'addr': u'empowerment@consumerfinance.gov'}], u'status': u'publish', u'parent': 0, u'tags': [], 'phone': [], u'date': u'2015-04-19T23:47:14-0500', u'slug': u'your-money-your-goals-toolkit', u'comment_status': u'closed', u'title_plain': u'Your Money, Your Goals Toolkit', u'url': u'http://www.consumerfinance.gov/contact/your-money-your-goals-toolkit/', u'title': u'Your Money, Your Goals Toolkit', u'modified': u'2015-04-27T10:55:34+0000', u'dek': u'', '_id': u'your-money-your-goals-toolkit', u'order': 0}
        output = contact.DataConverter().convert(imported_data)
        expected_output = {'body': u'<p>Your Money, Your Goals is a toolkit for social service organizations and others to use when working with low- and moderate-income and underserved consumers. The Office of Financial Empowerment can help you get started using YMYG in your work.</p>\n', 'contact_info-0-value-emails-0-order': u'0', 'contact_info-0-value-emails-count': '1', 'contact_info-0-type': u'email', 'contact_info-0-deleted': u'', 'contact_info-0-order': '0', 'contact_info-0-value-emails-0-value-url': u'empowerment@consumerfinance.gov', 'contact_info-0-value-emails-0-deleted': u'', 'contact_info-count': '1', 'heading': u'Your Money, Your Goals Toolkit;;your-money-your-goals-toolkit', 'contact_info-0-value-emails-0-value-text': u'email'}
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()

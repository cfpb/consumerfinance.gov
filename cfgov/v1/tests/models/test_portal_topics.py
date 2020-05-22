from django.test import TestCase

from v1.models.portal_topics import PortalCategory, PortalTopic


class TestPortalTagObjects(TestCase):

    fixtures = [
        'portal_categories.json', 'portal_topics.json', 'test_ask_tags.json'
    ]

    def test_portal_topic_string(self):
        portal_topic = PortalTopic.objects.order_by('heading').first()
        self.assertEqual(str(portal_topic), portal_topic.heading)

    def test_portal_category_string(self):
        portal_category = PortalCategory.objects.order_by('heading').first()
        self.assertEqual(str(portal_category), portal_category.heading)

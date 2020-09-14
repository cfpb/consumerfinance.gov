from django.test import TestCase, override_settings
from django.urls import reverse


class TestServiceWorkerView(TestCase):
    @override_settings(FLAGS={"MMT_MY_MONEY_CALENDAR": [("boolean", True)]})
    def test_service_worker(self):
        response = self.client.get(reverse('mmt-my-money-calendar'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response['content-type'], 'application/json')

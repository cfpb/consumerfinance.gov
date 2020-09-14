from django.test import TestCase
from django.urls import reverse


class TestServiceWorkerView(TestCase):
    def test_service_worker(self):
        response = self.client.get(reverse('my-money-calendar'))
        self.assertEqual(response.status_code, 200)

from django.test import TestCase
from django.urls import reverse

from wagtail.test.utils.wagtail_tests import WagtailTestUtils

from jobmanager.models import MajorCity, Region, State


class RegionViewSetTests(WagtailTestUtils, TestCase):
    def setUp(self):
        self.login()

    def test_region_viewset(self):
        usa = Region.objects.create(name="USA", abbreviation="us")
        texas = State.objects.create(
            name="Texas", abbreviation="TX", region_id=usa.pk
        )
        (
            State.objects.create(
                name="Utah", abbreviation="UT", region_id=usa.pk
            ),
        )
        MajorCity.objects.create(
            name="Dallas", state_id=texas.pk, region_id=usa.pk
        )
        MajorCity.objects.create(
            name="Houston", state_id=texas.pk, region_id=usa.pk
        )

        index_url = reverse("wagtailsnippets_jobmanager_region:list")
        response = self.client.get(index_url)

        self.assertContains(response, "Texas, Utah")
        self.assertContains(response, "Dallas, TX; Houston, TX")
